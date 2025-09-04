"""Define the resource used by Dagster jobs."""
from dagster import ConfigurableResource


DAG_CONFIG_KEY = "dag_config"
DATA_LAKE_KEY = "data_lake"
IDATA_IO_KEY = "idata_io_manager"
NOTIFIER_KEY = "scanhub_notifier"


class JobConfigResource(ConfigurableResource):
    """Resource used by the job."""

    callback_url: str | None = None
    user_access_token: str | None = None
    update_device_parameter_base_url: str | None = None
    input_files: list[str]
    output_dir: str
    task_id: str    # serves as series id
    exam_id: str    # serves as study id


class DAGConfiguration(ConfigurableResource):
    """Run-scoped parameters accessible from assets + IO managers."""

    output_directory: str = ""
    input_files: list[str] = []
    user_access_token: str = ""
    output_result_id: str = ""
