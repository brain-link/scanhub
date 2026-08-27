"""Dagster IO Manager for mrpro IData object."""
import shutil
from typing import List

from dagster import InputContext, OutputContext
from mrpro.data import IData
from upath import UPath

from orchestrator.io.base import ScanHubIOManager


class IDataIOManager(ScanHubIOManager):
    """IO manager for mrpro IData — writes DICOM files with Dagster run_id as filename prefix."""

    def dump_to_path(self, context: OutputContext, obj: IData, path: UPath) -> None:
        """Reconstruct IData to DICOM files inside the task directory.

        Files are saved as ``{run_id}_{index:04d}.dcm`` so that outputs from
        different Dagster runs of the same pipeline can coexist in the flat
        task directory and be traced back to a specific run.
        """
        run_id = context.run_id
        tmp_dir = path / f".tmp_{run_id}"
        path.mkdir(parents=True, exist_ok=True)  # ensure task dir exists; tmp_dir is created by to_dicom_folder

        try:
            obj.to_dicom_folder(str(tmp_dir))
            dcm_files = sorted(f for f in tmp_dir.iterdir() if f.suffix.lower() == ".dcm")
            output_files = []
            for idx, src in enumerate(dcm_files):
                dst = path / f"{run_id}_{idx:04d}.dcm"
                src.rename(dst)
                output_files.append(dst.name)
        finally:
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir)

        context.add_output_metadata({
            "task_dir": str(path),
            "run_id": run_id,
            "dicom_files": output_files,
            "num_files": len(output_files),
        })

    def load_from_path(self, context: InputContext, path: UPath) -> IData:
        """Load IData from the task directory."""
        return IData.from_dicom_folder(str(path))

    def load_from_files(self, files: List[str]) -> IData:
        """Load IData from an explicit file list."""
        if not files:
            return None
        return IData.from_dicom_folder(str(UPath(files[0]).parent))
