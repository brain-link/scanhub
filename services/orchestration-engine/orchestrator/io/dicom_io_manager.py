"""IO Manager for DICOM data."""
from typing import List

import pydicom
from dagster import InputContext, OutputContext
from upath import UPath

from orchestrator.io.base import ScanHubIOManager


class DicomIOManager(ScanHubIOManager):
    """IO manager for pydicom datasets — writes files with Dagster run_id as filename prefix."""

    def dump_to_path(self, context: OutputContext, obj: List[pydicom.Dataset], path: UPath) -> None:
        """Save DICOM datasets to the task directory as ``{run_id}_{index:04d}.dcm``."""
        if not isinstance(obj, list):
            obj = [obj]

        path.mkdir(parents=True, exist_ok=True)
        run_id = context.run_id
        output_files = []

        for idx, ds in enumerate(obj):
            filename = f"{run_id}_{idx:04d}.dcm"
            filepath = path / filename
            ds.save_as(str(filepath))
            output_files.append(filename)

        context.add_output_metadata({
            "task_dir": str(path),
            "run_id": run_id,
            "dicom_files": output_files,
            "num_files": len(output_files),
        })

    def load_from_path(self, context: InputContext, path: UPath) -> List[pydicom.Dataset]:
        """Load all DICOM files from the task directory."""
        if not path.exists() or not path.is_dir():
            return []
        return [
            pydicom.dcmread(str(p))
            for p in sorted(path.iterdir())
            if p.is_file() and p.suffix.lower() == ".dcm"
        ]

    def load_from_files(self, files: List[str]) -> List[pydicom.Dataset]:
        """Load DICOM datasets from an explicit file list."""
        return [pydicom.dcmread(f) for f in files]
