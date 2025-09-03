"""Definition of dagster data lake ressource for acquisition data."""
import json
from pathlib import Path

from dagster import ConfigurableResource


class DataLakeResource(ConfigurableResource):
    """Dagster data lake ressource."""

    def get_mrd_path(self, directory: str, filenames: list[str]) -> Path:
        """Construct and validate the MRD path inside the data lake.

        Parameters
        ----------
        directory : str
            Absolute path to result data (contains data lake path).
        filenames: list[str]
            List of filenames which can be found in directory.

        Returns
        -------
        path
            Path to acquisition ISMRMRD file.

        """
        filename = next((f for f in filenames if f.lower().endswith(".mrd")), None)
        if filename is None:
            raise FileNotFoundError(f"Acquisition result does not specify mrd filename.")
        mrd_path = Path(directory) / filename
        if not mrd_path.is_file():
            raise FileNotFoundError(f"MRD file does not exist: {mrd_path}")
        return mrd_path

    def get_device_parameter(self, directory: str, filenames: list[str]) -> dict:
        """Return the path to the device parameter JSON file if it exists.

        Parameters
        ----------
        directory : str
            Absolute path to result data (contains data lake path).
        filenames: list[str]
            List of filenames which can be found in directory.

        Returns
        -------
        dict
            Dictionary containing device parameters

        """
        filename = next((f for f in filenames if f.lower().endswith(".json")), None)
        if filename is None:
            raise FileNotFoundError(f"Acquisition result does not specify device parameter file.")
        json_path = Path(directory) / filename
        # Check if parameter file exists
        if not json_path.exists():
            raise FileExistsError(f"Device parameter file does not exist: {json_path}")
        # Load parameter file
        with json_path.open("r") as fh:
            data = json.load(fh)
        # Check if parameter file contains device id and parameter
        if "device_id" not in data or "parameter" not in data:
            raise AttributeError(f"Invalid paraeter file: {json_path}")
        return data
