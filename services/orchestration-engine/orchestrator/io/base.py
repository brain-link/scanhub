"""Base IO Manager for ScanHub resources."""
from abc import abstractmethod
from typing import Any, List

from dagster import ConfigurableIOManager, InputContext, OutputContext
from upath import UPath

from orchestrator.utils.dag_config import DAGConfiguration


class ScanHubIOManager(ConfigurableIOManager):
    """Base ConfigurableIOManager for ScanHub — resolves the task directory from dag_config."""

    dag_config: DAGConfiguration

    def _get_path(self) -> UPath:
        if not self.dag_config.task_dir:
            raise ValueError("task_dir is not set in dag_config.")
        return UPath(self.dag_config.task_dir)

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        if obj is None:
            return
        self.dump_to_path(context, obj, self._get_path())

    def load_input(self, context: InputContext) -> Any:
        return self.load_from_path(context, self._get_path())

    @abstractmethod
    def dump_to_path(self, context: OutputContext, obj: Any, path: UPath) -> None:
        """Write obj to path."""

    @abstractmethod
    def load_from_path(self, context: InputContext, path: UPath) -> Any:
        """Load object from path."""

    @abstractmethod
    def load_from_files(self, files: List[str]) -> Any:
        """Load object from an explicit file list."""
