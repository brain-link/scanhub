"""Definition of acquisiton data assets."""
from dataclasses import dataclass
from pathlib import Path

from dagster import AssetExecutionContext, MetadataValue, OpExecutionContext, asset, op
from scanhub_libraries.resources.dag_config import DAGConfiguration
from scanhub_libraries.resources.data_lake import DataLakeResource


@dataclass
class AcquisitionData:
    """Acquisition data output of read acquisition data asset."""

    mrd_path: Path
    device_id: str
    device_parameter: dict


def _load_acquisition_data(dag_config: DAGConfiguration, data_lake: DataLakeResource) -> AcquisitionData:
    """Load acquisition data."""
    mrd_file = data_lake.get_mrd_path(dag_config.input_files)
    device_id, device_parameter = data_lake.get_device_parameter(dag_config.input_files)
    return AcquisitionData(mrd_path=mrd_file, device_id=device_id, device_parameter=device_parameter)


@asset(
    group_name="io",
    description="Provides acquired ISMRMRD result",
)
def acquisition_data_asset(
    context: AssetExecutionContext,
    dag_config: DAGConfiguration,
    data_lake: DataLakeResource,
) -> AcquisitionData:
    """Define acquisition result asset."""
    data = _load_acquisition_data(dag_config, data_lake)
    context.log.info("Parameters for device id %s: %s", data.device_id, data.device_parameter)

    # Optional: Add meta data for dagster UI
    context.add_output_metadata({
        "mrd_path": MetadataValue.path(str(data.mrd_path)),
        "device_parameter": MetadataValue.json(data.device_parameter),
        "num_input_files": len(dag_config.input_files),
        "output_directory": MetadataValue.path(dag_config.output_directory),
        "output_result_id": dag_config.output_result_id,
        "access_token": dag_config.user_access_token,
    })
    return data


@op
def acquisition_data_op(
    context: OpExecutionContext,
    dag_config: DAGConfiguration,
    data_lake: DataLakeResource,
) -> AcquisitionData:
    """Op version of the loader so the job can run end-to-end without assets."""
    data = _load_acquisition_data(dag_config, data_lake)
    context.log.info("MRD file path: %s", str(data.mrd_path))
    context.log.info("Parameters for device id %s: %s", data.device_id, data.device_parameter)
    return data
