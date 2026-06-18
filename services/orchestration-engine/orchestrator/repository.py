# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Define dagster repository."""
import os

from dagster import AssetSelection, Definitions, define_asset_job, in_process_executor
from scanhub_libraries.resources import (
    DAG_CONFIG_KEY,
    DATA_LAKE_KEY,
    DICOM_IO_KEY,
    IDATA_IO_KEY,
    NOTIFIER_DM_KEY,
    NOTIFIER_EM_KEY,
)
from scanhub_libraries.resources.dag_config import DAGConfiguration
from scanhub_libraries.resources.data_lake import DataLakeResource
from scanhub_libraries.resources.notifier import DeviceManagerNotifier, ProtocolManagerNotifier

from orchestrator.assets.acquisition_data import acquisition_data_asset
from orchestrator.assets.dicom_input import dicom_input
from orchestrator.assets.image_processing import image_smoothing
from orchestrator.assets.mrpro_direct_reconstruction import mrpro_direct_reconstruction
from orchestrator.io.dicom_io_manager import DicomIOManager
from orchestrator.io.idata_io_manager import IDataIOManager
from orchestrator.jobs.mri_frequency_calibration import frequency_calibration_job
from orchestrator.sensors import on_run_canceled, on_run_failure, on_run_success

DATA_LAKE_DIR = os.getenv("DATA_LAKE_DIRECTORY", "data")
EXAM_MANAGER_URI = "http://protocol-manager:8000/api/v1/protocol"
DEVICE_MANAGER_URI = "http://device-manager:8000/api/v1/device"


assets = [
    acquisition_data_asset,
    mrpro_direct_reconstruction,
    dicom_input,
    image_smoothing,
]

sensors = [
    on_run_success,
    on_run_failure,
    on_run_canceled,
]

_dag_config = DAGConfiguration.configure_at_launch()

ressources = {
    DAG_CONFIG_KEY: _dag_config,
    DATA_LAKE_KEY: DataLakeResource.configure_at_launch(),
    IDATA_IO_KEY: IDataIOManager(dag_config=_dag_config),
    DICOM_IO_KEY: DicomIOManager(dag_config=_dag_config),
    NOTIFIER_EM_KEY: ProtocolManagerNotifier(base_url=EXAM_MANAGER_URI),
    NOTIFIER_DM_KEY: DeviceManagerNotifier(base_url=DEVICE_MANAGER_URI),
}

jobs = (
    define_asset_job(
        name="mrpro_reconstruction_job",
        selection=AssetSelection.keys(acquisition_data_asset.key, mrpro_direct_reconstruction.key),
    ),
    frequency_calibration_job,
    define_asset_job(
        name="image_smoothing_job",
        selection=AssetSelection.keys(image_smoothing.key),
    ),
)

defs = Definitions(assets=assets, resources=ressources, jobs=jobs, sensors=sensors, executor=in_process_executor)
