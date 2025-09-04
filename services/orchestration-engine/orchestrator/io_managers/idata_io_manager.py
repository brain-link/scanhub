"""Dagster IO Manager for mrpro IData object."""
from dataclasses import dataclass
from pathlib import Path

from dagster import ConfigurableIOManager, InputContext, OutputContext
from mrpro.data import IData
from scanhub_libraries.resources import DAGConfiguration


@dataclass
class IDataContext:
    """Context definition for IData IO manager."""

    data: IData
    dag_config: DAGConfiguration


class IDataIOManager(ConfigurableIOManager):
    """IO manager for mrpro IData object."""

    def handle_output(self, context: OutputContext, obj: IDataContext) -> None:
        """Write idata to dicom folder."""
        # Decide where to write based on asset key
        if not obj.dag_config.output_directory:
            context.log.error("Output directory not defined")
            raise AttributeError
        directory_path = Path(obj.dag_config.output_directory)

        obj.data.to_dicom_folder(directory_path)

        # Surface paths in the UI and for hooks/sensors
        context.add_output_metadata({
            "output_directory": str(directory_path.resolve()),
            "stored_files": [p.name for p in directory_path.iterdir() if p.is_file()],
        })

    def load_input(self, context: InputContext) -> IData:
        """Read idata from dicom folder."""
        if (meta := context.metadata) is None:
            context.log.error("No metadata, cannot save result")
            raise AttributeError
        dcm_folder = meta.get("output_directory")
        if not dcm_folder:
            context.log.error("Missing directory to load dicom files")
            raise AttributeError
        dcm_path = Path(dcm_folder)
        if not dcm_path.exists():
            msg = f"DICOM folder does not exist: {dcm_path}"
            context.log.error(msg)
            raise FileNotFoundError(msg)
        return IData.from_dicom_folder(str(dcm_path))
