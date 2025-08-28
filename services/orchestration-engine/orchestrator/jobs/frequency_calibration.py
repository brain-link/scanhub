# %%
import json
import tempfile
from pathlib import Path

from dagster import RunConfig, graph, op
from scanhub_libraries.resources import SCANHUB_RESOURCE_KEY, JobConfigResource

from orchestrator.ops.scanhub import notify_op, send_device_parameter_update


@op(required_resource_keys={SCANHUB_RESOURCE_KEY})
def load_parameter(context) -> dict | None:
    """Load device parameter file."""
    job_config: JobConfigResource = context.resources.job_config
    # Get correct input:
    parameter_file = None
    for _file in job_config.input_files:
        if _file.endswith(".json"):
            parameter_file = Path(_file)
            if not parameter_file.exists():
                context.log.error("Parameter file does not exist")

    if parameter_file is not None:
        with parameter_file.open("r") as fh:
            data = json.load(fh)

        if "device_id" not in data or "parameter" not in data:
            context.log.error("Invalid parameter file")

        context.log.info("Loaded parameter file: %s", data)
        return data

    context.log.error("No parameter file found in job input files.")
    return None


@op
def update_parameters(context, data: dict) -> dict:
    """Modify device parameter."""
    context.log.info("Device ID: %s", data["device_id"])
    context.log.info("Parameter: %s", data["parameter"])
    data["parameter"]["larmor_frequency"] += 10
    context.log.info("Updated parameter: %s", data["parameter"])
    return data


@graph
def frequency_calibration_graph() -> None:
    """Define frequency calibration graph."""
    data = load_parameter()
    if data is not None:
        data = update_parameters(data)
        done = send_device_parameter_update(data)
        notify_op(done)

# Define the job with the resource definition (uses defaults here)
frequency_calibration_job = frequency_calibration_graph.to_job(
    name="frequency_calibration_job",
    resource_defs={SCANHUB_RESOURCE_KEY: JobConfigResource.configure_at_launch()},
)

# %%
if __name__ == "__main__":
    print("Testing frequency calibration job...")
    data = {'device_id': 'f977740a-5ddf-4364-9a40-941cd49d5050', 'parameter': {'larmor_frequency': 2025000.0}}
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "device_config.json"
        with file_path.open("w") as fh:
            json.dump(data, fh)

        result = frequency_calibration_job.execute_in_process(
            run_config=RunConfig(
                resources={
                    SCANHUB_RESOURCE_KEY: JobConfigResource(
                        callback_url=None,
                        user_access_token=None,
                        input_files=[str(file_path)],
                        output_dir=tmpdir + "/output",
                        update_device_parameter_base_url=None,
                        task_id="",
                        exam_id="",
                    )
                },
                loggers={"console": {"config": {"log_level": "INFO"}}},
            )
        )

    # Report logs
    for event in result.all_events:
        print(f"{event.event_type_value} > {event.message}")


# %%
