# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of acquisition data asset."""
from dataclasses import dataclass
from pathlib import Path

from dagster import AssetExecutionContext, MetadataValue, asset
from scanhub_libraries.resources.dag_config import DAGConfiguration
from scanhub_libraries.resources.data_lake import DataLakeResource


@dataclass
class AcquisitionData:
    """Acquisition data output of read acquisition data asset."""

    mrd_path: Path
    device_id: str
    device_parameter: dict


@asset(
    group_name="io",
    description="Loads acquisition data (MRD + device parameters) from the task directory.",
)
def acquisition_data_asset(
    context: AssetExecutionContext,
    dag_config: DAGConfiguration,
    data_lake: DataLakeResource,
) -> AcquisitionData:
    """Load MRD file and device parameters from the flat task directory."""
    mrd_path = data_lake.get_mrd_path(dag_config.task_dir)
    device_id, device_parameter = data_lake.get_device_parameter(dag_config.task_dir)

    context.log.info("Task dir: %s", dag_config.task_dir)
    context.log.info("MRD path: %s", str(mrd_path))
    context.log.info("Device %s parameters: %s", device_id, device_parameter)

    context.add_output_metadata({
        "task_dir": MetadataValue.path(dag_config.task_dir),
        "mrd_path": MetadataValue.path(str(mrd_path)),
        "device_id": device_id,
        "device_parameter": MetadataValue.json(device_parameter),
    })
    return AcquisitionData(mrd_path=mrd_path, device_id=device_id, device_parameter=device_parameter)
