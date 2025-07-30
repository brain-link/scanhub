"""Reconstruction from k-space numpy array to dicom image using numpy FFT."""
# %%
# Imports
import os
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pydicom
import pydicom._storage_sopclass_uids
import requests
from airflow import DAG
from airflow.decorators import task
from pydicom.dataset import Dataset

# %%

default_args = {
    'owner': 'BRAIN-LINK',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='dag_reco_v01',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['scanhub', 'reconstruction']
) as dag:
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    @task(multiple_outputs=True)
    def fft_reconstruction():
        # Check input file
        input_file_path = Path(INPUT_DIR) / INPUT_FILE
        if not input_file_path.suffix == "mrd":
            raise FileNotFoundError(f"Invalid file format: {input_file_path}")

        # Load data and reconstruct k-space
        kspace = np.load(input_file_path)
        print(f"Loaded k-space with shape {kspace.shape} and dtype {kspace.dtype} from file: {input_file_path}")

        image = np.fft.ifftshift(np.fft.ifftn(np.fft.fftshift(kspace)))
        image_f16 = np.abs(image).astype(np.float16)

        # Write image data to dicom
        meta = pydicom.Dataset()
        # pylint: disable=protected-access
        meta.FileMetaInformationGroupLength = 212
        meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
        meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
        meta.SourceApplicationEntityTitle = "BRAIN-LINK"

        dicom_dataset = Dataset()
        dicom_dataset.file_meta = meta  # type: ignore

        dicom_dataset.is_little_endian = True
        dicom_dataset.is_implicit_VR = False

        # pylint: disable=protected-access
        dicom_dataset.SOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
        dicom_dataset.PatientName = "Max^Mustermann"
        dicom_dataset.PatientID = "123456"

        dicom_dataset.Modality = "MR"
        dicom_dataset.SeriesInstanceUID = pydicom.uid.generate_uid()
        dicom_dataset.StudyID = pydicom.uid.generate_uid()
        dicom_dataset.SOPInstanceUID = pydicom.uid.generate_uid()
        dicom_dataset.StudyInstanceUID = pydicom.uid.generate_uid()
        dicom_dataset.FrameOfReferenceUID = pydicom.uid.generate_uid()

        dicom_dataset.BitsStored = 16
        dicom_dataset.BitsAllocated = 16
        dicom_dataset.SamplesPerPixel = 1
        dicom_dataset.HighBit = 15

        dicom_dataset.ImagesInAcquisition = "1"

        dicom_dataset.Rows = image_f16.shape[0]
        dicom_dataset.Columns = image_f16.shape[1]
        dicom_dataset.InstanceNumber = 1

        dicom_dataset.ImagePositionPatient = r"0\0\1"
        dicom_dataset.ImageOrientationPatient = r"1\0\0\0\-1\0"
        dicom_dataset.ImageType = r"ORIGINAL\PRIMARY\AXIAL"

        dicom_dataset.RescaleIntercept = "0"
        dicom_dataset.RescaleSlope = "1"
        dicom_dataset.PixelSpacing = r"1\1"
        dicom_dataset.PhotometricInterpretation = "MONOCHROME2"
        dicom_dataset.PixelRepresentation = 1

        pydicom.dataset.validate_file_meta(dicom_dataset.file_meta, enforce_standard=True)

        print("Setting pixel data...")
        dicom_dataset.PixelData = image_f16.tobytes()

        # Save as DICOM
        print("Saving file...")
        output_file_path = input_file_path.parent / (RESULT_ID + ".dcm")
        dicom_dataset.save_as(output_file_path)

        # Convert from dicom to dicom with gdcmconv to add P10 header -> temporary fix
        cmd = f"gdcmconv -C {output_file_path} {output_file_path}"
        os.system(cmd)  # noqa: S605  # returns the exit code in unix

        return output_file_path

    @task()
    def notify_workflow_manager(output_file):
        print("Submitting output file: ", output_file)
        if USER_TOKEN is not None:
            response = requests.post(WORKFLOW_MANAGER_CALLBACK, headers={"Authorization": "Bearer " + USER_TOKEN}, timeout=3)
            print(response)

    # Define the file paths
    INPUT_DIR = '{{ dag_run.conf["directory"] }}'
    INPUT_FILE = '{{ dag_run.conf["file_name"] }}'
    RESULT_ID = '{{ dag_run.conf["result_id"] }}'
    WORKFLOW_MANAGER_CALLBACK = '{{ dag_run.conf["workflow_manager_endpoint"] }}'
    USER_TOKEN = '{{ dag_run.conf["user_token"] }}'

    # Define the task dependencies
    output_file = fft_reconstruction()
    notify_workflow_manager(output_file)


# %%
if __name__ == "__main__":
    dag.test(
        logical_date=datetime(2025, 1, 1),
        run_conf={
            "result_id": "some ID",
            "directory": "/data_lake/c688c04b-8462-4c65-bdc5-6aa6327c46a9",
            "file_name": "c06c099f-2035-4739-b74f-9cf9daf80e1f.npy",
            "workflow_manager_endpoint": "https://localhost:8443/api/v1/workflowmanager/result_ready/d50df8d3-290d-4813-aac9-35df536271e3",
            "user_token": None,
        }
    )

# %%
