"""Define dagster repository."""
from dagster import repository

from dagster_workflows.image_processing_job import processing_job
from dagster_workflows.numpy_image_reconstruction import reconstruct_job
from dagster_workflows.mrpro_image_reconstruction import mrpro_reconstruction_job


@repository
def reconstruction_repository() -> list:
    """Define the reconstruction repository."""
    return [
        reconstruct_job,
        mrpro_reconstruction_job,
    ]


@repository
def processing_repository() -> list:
    """Define the processing repository."""
    return [
        processing_job,
        # more jobs...
    ]
