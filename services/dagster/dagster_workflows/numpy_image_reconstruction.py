# %%
import tempfile
from pathlib import Path
from scanhub_libraries.resources import JobConfigResource, SCANHUB_RESOURCE_KEY

import numpy as np
import requests
from dagster import (
    op, graph, RunConfig, OpExecutionContext, In, Out, Nothing
)


@op(required_resource_keys={SCANHUB_RESOURCE_KEY})
def load_data(context: OpExecutionContext) -> np.ndarray:
    job_config: JobConfigResource = context.resources.job_config
    path = Path(job_config.input_file)
    context.log.info(f"Loading data from {path}")
    data = np.load(path)
    context.log.info(f"Loaded data: {data.shape} - dtype: {data.dtype}")
    return data


@op
def numpy_fft(context: OpExecutionContext, data: np.ndarray) -> np.ndarray:
    context.log.info("Computing FFT...")
    data_fft = np.fft.ifftshift(np.fft.ifftn(np.fft.fftshift(data)))
    return data_fft


@op(required_resource_keys={SCANHUB_RESOURCE_KEY}, out=Out(Nothing))
def save_data(context: OpExecutionContext, data: np.ndarray) -> None:
    job_config: JobConfigResource = context.resources.job_config
    path = Path(job_config.output_dir)
    path.mkdir(parents=True, exist_ok=True)
    context.log.info(f"Saving data to {path}")
    np.save(path / "image.npy", data)
    context.log.info(f"Saved data: {data.shape} - dtype: {data.dtype}")
    return


@op(required_resource_keys={SCANHUB_RESOURCE_KEY}, ins={"after_save": In(Nothing)})
def notify_op(context: OpExecutionContext) -> None:
    job_config: JobConfigResource = context.resources.job_config
    if job_config.callback_url and job_config.user_access_token:
        try:
            headers = {"Authorization": "Bearer " + job_config.user_access_token}
            callback_response = requests.post(job_config.callback_url, headers=headers, timeout=3)
            if callback_response.status_code != 200:
                context.log.error(f"Callback failed with status code {callback_response.status_code}")
            else:
                context.log.info("Callback successful")
        except Exception as e:
            context.log.error(f"Callback failed: {e}")


@graph
def reconstruct_graph():
    data = load_data()
    result = numpy_fft(data)
    done = save_data(result)
    notify_op(done)

# Define the job with the resource definition (uses defaults here)
reconstruct_job = reconstruct_graph.to_job(
    name="reconstruct_job",
    resource_defs={SCANHUB_RESOURCE_KEY: JobConfigResource.configure_at_launch()},
)

# %%
if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "in.npy"
        # Generate some complex valued dummy data
        np.save(input_path, np.random.rand(1, 60, 60) + 1j * np.random.rand(1, 60, 60))

        reconstruct_job.execute_in_process(
            run_config=RunConfig(resources={
                SCANHUB_RESOURCE_KEY: JobConfigResource(
                    callback_url=None,
                    user_access_token=None,
                    input_file=str(input_path),
                    output_dir=tmpdir,
                )
            })
        )

        data_in = np.load(input_path)
        data_out = np.load(output_path)
        print(f"Input data:\t{data_in.shape} - dtype: {data_in.dtype}")
        print(f"Output data:\t{data_out.shape} - dtype: {data_out.dtype}")
# %%
