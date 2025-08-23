"""Define dagster repository."""
from dagster import repository

from dagster_workflows.frequency_calibration import frequency_calibration_job
from dagster_workflows.mrpro_image_reconstruction import mrpro_reconstruction_job


@repository
def reconstruction_repository() -> list:
    """Define the reconstruction repository."""
    return [
        mrpro_reconstruction_job,
    ]


@repository
def processing_repository() -> list:
    """Define the processing repository."""
    return [
        frequency_calibration_job,
    ]
