# %%
import tempfile
from pathlib import Path

import mrpro
from dagster import Nothing, OpExecutionContext, Out, RunConfig, graph, op
from scanhub_libraries.resources import SCANHUB_RESOURCE_KEY, JobConfigResource

from dagster_workflows.shared_ops import notify_op


@op(required_resource_keys={SCANHUB_RESOURCE_KEY})
def load_kdata(context: OpExecutionContext) -> mrpro.data.KData:
    """Load k-space data from MRD file."""
    job_config: JobConfigResource = context.resources.job_config
    path = Path(job_config.input_files[0])  # expect a single input file
    context.log.info("Loading data from %s", path)

    if not path.exists():
        detail = f"Input file {path} does not exist"
        context.log.error(detail)
        raise FileNotFoundError(detail)

    # trajectory_calculator = mrpro.data.traj_calculators.KTrajectoryIsmrmrd()
    trajectory_calculator = mrpro.data.traj_calculators.KTrajectoryCartesian()
    kdata = mrpro.data.KData.from_file(path, trajectory_calculator)
    context.log.info("Loaded data: %s", kdata.shape)

    return kdata


@op
def direct_reconstruction(context: OpExecutionContext, kdata: mrpro.data.KData) -> mrpro.data.IData:
    """Perform direct reconstruction on k-space data."""
    context.log.info("Performing direct reconstruction using mrpro...")

    reconstruction = mrpro.algorithms.reconstruction.DirectReconstruction(kdata)

    return reconstruction(kdata)


@op(required_resource_keys={SCANHUB_RESOURCE_KEY}, out=Out(Nothing))
def save_as_dicom(context: OpExecutionContext, img: mrpro.data.IData) -> None:
    """Save reconstructed image as DICOM files."""
    job_config: JobConfigResource = context.resources.job_config
    path = Path(job_config.output_dir)
    if path.exists():
        context.log.info("Output directory %s already exists, removing it.", path)
        for item in path.iterdir():
            if item.is_file():
                item.unlink()
            else:
                item.rmdir()

    context.log.info("Saving dicom files to %s", path)
    img.to_dicom_folder(path)
    context.log.info("Data saved successfully.")
    return


@graph
def mrpro_reconstruct_graph() -> None:
    """Graph for MRPro image reconstruction."""
    ksp = load_kdata()
    img = direct_reconstruction(ksp)
    done = save_as_dicom(img)
    notify_op(done)


# Define the job with the resource definition (uses defaults here)
mrpro_reconstruction_job = mrpro_reconstruct_graph.to_job(
    name="mrpro_direct_reconstruct_job",
    resource_defs={SCANHUB_RESOURCE_KEY: JobConfigResource.configure_at_launch()},
)

# %%
if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = "../../../tools/examples/data.mrd"

        result = mrpro_reconstruction_job.execute_in_process(
            run_config=RunConfig(resources={
                SCANHUB_RESOURCE_KEY: JobConfigResource(
                    callback_url=None,
                    user_access_token=None,
                    input_files=[str(input_path)],
                    output_dir=tmpdir + "/output",  # Ensure output directory is specified
                    task_id="",
                    exam_id="",
                    update_device_parameter_base_url=None,
                )
            })
        )

    # Report logs
    for event in result.all_events:
        print(f"{event.event_type_value} > {event.message}")

# %%
