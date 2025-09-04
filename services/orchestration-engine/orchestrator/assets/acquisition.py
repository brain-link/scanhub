"""Definition of acquisiton data assets."""
from dataclasses import dataclass
from pathlib import Path

from dagster import AssetExecutionContext, MetadataValue, asset
from scanhub_libraries.resources import DAGConfiguration

from orchestrator.ressources.datalake import DataLakeResource


@dataclass
class AcquisitionData:
    """Acquisition data output of read acquisition data asset."""

    mrd_path: Path
    device_parameter: dict


@asset(
    group_name="io",
    description="Provides acquired ISMRMRD result",
)
def read_acquisition_data(
    context: AssetExecutionContext,
    dag_config: DAGConfiguration,
    data_lake: DataLakeResource,
) -> AcquisitionData:
    """Define acquisition result asset."""
    mrd_file = data_lake.get_mrd_path(dag_config.input_files)
    context.log.info("MRD file path: %s", str(mrd_file))
    device_parameter = data_lake.get_device_parameter(dag_config.input_files)
    context.log.info("Device parameters: %s", str(device_parameter))

    # Optional: surface helpful metadata in the Dagster UI
    context.add_output_metadata({
        "mrd_path": MetadataValue.path(str(mrd_file)),
        "device_parameter": MetadataValue.json(device_parameter),
        "num_input_files": len(dag_config.input_files),
        "output_directory": MetadataValue.path(dag_config.output_directory),
        "output_result_id": dag_config.output_result_id,
        "access_token": dag_config.user_access_token,
    })

    return AcquisitionData(mrd_path=mrd_file, device_parameter=device_parameter)
