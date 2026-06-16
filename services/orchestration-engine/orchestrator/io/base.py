"""Base IO Manager for ScanHub resources."""
from abc import ABC, abstractmethod
from typing import Any, List

from dagster import InputContext, OutputContext, UPathIOManager
from upath import UPath


class ScanHubIOManager(UPathIOManager, ABC):
    """Base IO Manager for ScanHub using UPathIOManager."""

    def _get_path(self, context: InputContext | OutputContext) -> UPath:
        """Resolve the path for an asset to the flat task directory."""
        if not hasattr(context.resources, "dag_config"):
            raise RuntimeError("dag_config resource not found in context.")
        dag_config = context.resources.dag_config
        if not dag_config.task_dir:
            raise ValueError("task_dir is not set in dag_config.")
        return UPath(dag_config.task_dir)

    @abstractmethod
    def load_from_files(self, files: List[str]) -> Any:
        """Load object from a specific list of files."""

    def load_input(self, context: InputContext) -> Any:
        """Load input via standard UPath behaviour."""
        return super().load_input(context)
