"""Define the resource used by Dagster jobs."""
from dagster import ConfigurableResource


class DAGConfiguration(ConfigurableResource):
    """Run-scoped parameters accessible from assets and IO managers."""

    task_dir: str = ""           # absolute path to {DATA_LAKE_DIR}/{workflow_id}/{task_id}/
    task_id: str = ""
    workflow_id: str = ""
    user_access_token: str = ""
