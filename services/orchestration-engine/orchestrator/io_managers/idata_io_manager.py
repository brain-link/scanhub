"""Dagster IO Manager for mrpro IData object."""
from pathlib import Path

from dagster import IOManager, OutputContext, InputContext, io_manager
from mrpro.data import IData


class IDataIOManager(IOManager):
    """IO manager for mrpro IData object."""

    def __init__(self, base_dir: str) -> None:
        """Init."""
        self.base_dir = Path(base_dir)

    def handle_output(self, context: OutputContext, idata: IData) -> None:
        """Write idata to dicom folder."""
        # Decide where to write based on asset key
        asset_key = "_".join(context.asset_key.path)
        output_dir = self.base_dir / asset_key
        output_dir.mkdir(parents=True, exist_ok=False)

        idata.to_dicom_folder(output_dir)

        context.add_output_metadata({
            "stored_files": [f.name for f in output_dir.iterdir() if f.is_file()],
            "output_dir": str(output_dir),
        })

    def load_input(self, context: InputContext) -> IData:
        """Read idata from dicom folder."""
        # Reload previously written files if needed
        upstream_metadata = context.upstream_output.metadata
        dcm_folder = Path(upstream_metadata.get("output_dir"))
        if not dcm_folder.exists():
            context.log.error("Dicom folder does not exist: %s", dcm_folder)
        return IData.from_dicom_folder(dcm_folder)


@io_manager(config_schema={"base_dir": str})
def idata_io_manager(init_context) -> IDataIOManager:
    return IDataIOManager(base_dir=init_context.resource_config["base_dir"])
