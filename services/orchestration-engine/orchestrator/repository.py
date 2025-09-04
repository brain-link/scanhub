"""Define dagster repository."""
import os

from dagster import AssetSelection, Definitions, define_asset_job, in_process_executor

# from orchestrator.jobs.frequency_calibration import frequency_calibration_job
# from orchestrator.jobs.mrpro_image_reconstruction import mrpro_reconstruction_job
from orchestrator.assets.acquisition import read_acquisition_data
from orchestrator.assets.mrpro_direct_reconstruction import mrpro_direct_reconstruction
from orchestrator.io_managers.idata_io_manager import IDataIOManager
from orchestrator.ressources.datalake import DataLakeResource
from orchestrator.ressources.notifier import BackendNotifier
from scanhub_libraries.resources import DAGConfiguration, DAG_CONFIG_KEY, IDATA_IO_KEY, DATA_LAKE_KEY, NOTIFIER_KEY

DATA_LAKE_DIR = os.getenv("DATA_LAKE_DIRECTORY", "data")
# if DATA_LAKE_DIR is None:   # ensure that DATA_LAKE_DIR is set
#     raise OSError("Missing `DATA_LAKE_DIRECTORY` environment variable.")


assets = [
    read_acquisition_data,
    mrpro_direct_reconstruction,
]

ressources = {
    DAG_CONFIG_KEY: DAGConfiguration(),
    DATA_LAKE_KEY: DataLakeResource(),
    IDATA_IO_KEY: IDataIOManager(),
    NOTIFIER_KEY: BackendNotifier(),
}

jobs = [
    define_asset_job(
        name="mrpro_reconstruction_job",
        selection=AssetSelection.keys("read_acquisition_data", "mrpro_direct_reconstruction"),
        # selection=[dg.AssetSelection.keys("reconstruct_numpy")],
        # tags={"workflow_id": "numpy"},
    ),
]

defs = Definitions(assets=assets, resources=ressources, jobs=jobs, executor=in_process_executor)
