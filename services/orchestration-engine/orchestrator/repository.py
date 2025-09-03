"""Define dagster repository."""
import os

from dagster import Definitions, in_process_executor

from orchestrator.assets.acquisition import acquisition_results
from orchestrator.io_managers.idata_io_manager import idata_io_manager
# from orchestrator.jobs.frequency_calibration import frequency_calibration_job
# from orchestrator.jobs.mrpro_image_reconstruction import mrpro_reconstruction_job
from orchestrator.jobs.mrpro_reco_asset_job import mrpro_direct_reconstructed_dcm, mrpro_direct_reconstruction_job
from orchestrator.ressources.datalake import DataLakeResource

DATA_LAKE_DIR = os.getenv("DATA_LAKE_DIRECTORY", "data")
# if DATA_LAKE_DIR is None:   # ensure that DATA_LAKE_DIR is set
#     raise OSError("Missing `DATA_LAKE_DIRECTORY` environment variable.")


definitions = Definitions(
    assets=[
        acquisition_results,
        mrpro_direct_reconstructed_dcm,
    ],
    resources={
        "datalake": DataLakeResource(),
        "idata_io_manager": idata_io_manager.configured({"base_dir": DATA_LAKE_DIR}),
    },
    jobs=[
        mrpro_direct_reconstruction_job,
        # mrpro_reconstruction_job,
        # frequency_calibration_job,
    ],
    executor=in_process_executor,   # default executor for all jobs
)
