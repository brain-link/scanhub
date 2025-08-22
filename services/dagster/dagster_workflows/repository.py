"""Define dagster repository."""
from dagster import Definitions, in_process_executor

from dagster_workflows.frequency_calibration import frequency_calibration_job
from dagster_workflows.mrpro_image_reconstruction import mrpro_reconstruction_job

definitions = Definitions(
    jobs=[
        mrpro_reconstruction_job,
        frequency_calibration_job,
    ],
    executor=in_process_executor,   # default executor for all jobs
)
