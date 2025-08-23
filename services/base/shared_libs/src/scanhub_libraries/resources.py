"""Define the resource used by Dagster jobs."""
from dagster import ConfigurableResource


SCANHUB_RESOURCE_KEY = "job_config"


class JobConfigResource(ConfigurableResource):
    """Resource used by the job."""

    callback_url: str | None = None
    user_access_token: str | None = None
    input_files: list[str]
    output_dir: str
    task_id: str    # serves as series id
    exam_id: str    # serves as study id
    update_device_parameter_base_url: str | None = None
