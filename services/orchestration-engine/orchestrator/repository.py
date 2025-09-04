"""Define dagster repository."""
import os

from dagster import AssetSelection, Definitions, define_asset_job, in_process_executor
from scanhub_libraries.resources import DAG_CONFIG_KEY, DATA_LAKE_KEY, IDATA_IO_KEY, NOTIFIER_KEY
from scanhub_libraries.resources.dag_config import DAGConfiguration
from scanhub_libraries.resources.data_lake import DataLakeResource
from scanhub_libraries.resources.notifier import BackendNotifier

from orchestrator.assets.mrpro_direct_reconstruction import mrpro_direct_reconstruction
from orchestrator.io.acquisition_data import acquisition_data_asset
from orchestrator.io.idata_io_manager import IDataIOManager
from orchestrator.jobs.mri_calibration import frequency_calibration_job

DATA_LAKE_DIR = os.getenv("DATA_LAKE_DIRECTORY", "data")

assets = [
    acquisition_data_asset,
    mrpro_direct_reconstruction,
]

ressources = {
    DAG_CONFIG_KEY: DAGConfiguration.configure_at_launch(),
    DATA_LAKE_KEY: DataLakeResource.configure_at_launch(),
    IDATA_IO_KEY: IDataIOManager.configure_at_launch(),
    NOTIFIER_KEY: BackendNotifier.configure_at_launch(),
}

jobs = (
    define_asset_job(
        name="mrpro_reconstruction_job",
        selection=AssetSelection.keys(acquisition_data_asset.key, mrpro_direct_reconstruction.key),
        # selection=[dg.AssetSelection.keys("reconstruct_numpy")],
        # tags={"workflow_id": "numpy"},
    ),
    frequency_calibration_job,
)

defs = Definitions(assets=assets, resources=ressources, jobs=jobs, executor=in_process_executor)
