"""Define dagster repository."""
from dagster import Definitions, in_process_executor

from orchestrator.jobs.frequency_calibration import frequency_calibration_job
from orchestrator.jobs.mrpro_image_reconstruction import mrpro_reconstruction_job

defs = Definitions(
    jobs=[
        mrpro_reconstruction_job,
        frequency_calibration_job,
    ],
    executor=in_process_executor,   # default executor for all jobs
)



