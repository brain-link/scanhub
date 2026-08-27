"""Definition of dagster data lake resource for acquisition data."""
import json
from pathlib import Path

from dagster import ConfigurableResource


class DataLakeResource(ConfigurableResource):
    """Dagster data lake resource."""

    def get_mrd_path(self, task_dir: str) -> Path:
        """Find the MRD file inside a task directory.

        Parameters
        ----------
        task_dir
            Absolute path to the task data directory.

        Returns
        -------
        Path
            Path to the acquisition ISMRMRD file.
        """
        matches = [f for ext in ("*.mrd", "*.h5") for f in Path(task_dir).glob(ext)]
        if not matches:
            raise FileNotFoundError(f"No MRD file found in: {task_dir}")
        return matches[0]

    def get_device_parameter(self, task_dir: str) -> tuple[str, dict]:
        """Read device parameters from device_parameter.json inside a task directory.

        Parameters
        ----------
        task_dir
            Absolute path to the task data directory.

        Returns
        -------
        tuple[str, dict]
            Device ID and parameter dictionary.
        """
        param_file = Path(task_dir) / "device_parameter.json"
        if not param_file.exists():
            raise FileNotFoundError(f"device_parameter.json not found in: {task_dir}")
        with param_file.open("r") as fh:
            data = json.load(fh)
        if "device_id" not in data or "parameter" not in data:
            raise AttributeError(f"Invalid device_parameter.json in: {task_dir}")
        return str(data["device_id"]), data["parameter"]
