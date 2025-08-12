"""Define the resource used by Dagster jobs."""
from dagster import ConfigurableResource


SCANHUB_RESOURCE_KEY = "job_config"


class JobConfigResource(ConfigurableResource):
    """Resource used by the job."""

    callback_url: str | None = None
    user_access_token: str | None = None
    input_file: str
    output_dir: str
