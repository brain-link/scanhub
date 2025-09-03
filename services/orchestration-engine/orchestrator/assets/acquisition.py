"""Definition of acquisiton data assets."""
from typing import Generator

from dagster import DynamicOutput, MetadataValue, OpExecutionContext, asset
from scanhub_libraries.models import ResultOut


@asset(
    required_resource_keys={"datalake"},
    config_schema={"acquisitions": list},
)
def acquisition_results(context: OpExecutionContext) -> Generator[DynamicOutput]:
    """Define acquisition result asset."""
    for acq in context.op_config["acquisitions"]:
        result = ResultOut(**acq)
        context.log.info("Processing acquisition result: %s", result)
        mrd_file = context.resources.datalake.get_mrd_path(result.directory, result.files)
        context.log.info("MRD file path: %s", str(mrd_file))
        device_parameter = context.resources.datalake.get_device_parameter(result.directory, result.files)
        context.log.info("Device parameters: %s", str(device_parameter))

        yield DynamicOutput(
            value={
                "mrd_file": mrd_file,
                "device_parameter": device_parameter,
                "result": result.model_dump(),
            },
            mapping_key=str(result.id),
            metadata={
                "mrd_file": MetadataValue.path(str(mrd_file)),
                "result": MetadataValue.json(result.model_dump()),
                "device_parameter": MetadataValue.json(device_parameter),
            },
        )
