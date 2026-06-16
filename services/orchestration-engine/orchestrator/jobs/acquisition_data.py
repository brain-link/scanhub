# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of acquisition data operation."""
from dagster import OpExecutionContext, op
from scanhub_libraries.resources.dag_config import DAGConfiguration
from scanhub_libraries.resources.data_lake import DataLakeResource

from orchestrator.assets.acquisition_data import AcquisitionData


@op
def acquisition_data_op(
    context: OpExecutionContext,
    dag_config: DAGConfiguration,
    data_lake: DataLakeResource,
) -> AcquisitionData:
    """Load acquisition data (MRD + device parameters) from the flat task directory."""
    mrd_path = data_lake.get_mrd_path(dag_config.task_dir)
    device_id, device_parameter = data_lake.get_device_parameter(dag_config.task_dir)

    context.log.info("MRD file path: %s", str(mrd_path))
    context.log.info("Parameters for device id %s: %s", device_id, device_parameter)
    return AcquisitionData(mrd_path=mrd_path, device_id=device_id, device_parameter=device_parameter)
