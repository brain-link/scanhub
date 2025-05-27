# [START import_module]
import os
import json
import numpy as np


from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
import requests
from zipfile import ZipFile, is_zipfile

import pydicom
import pydicom._storage_sopclass_uids
from pydicom.dataset import Dataset

# [END import_module]

default_args = {
    'owner': 'BRAIN-LINK',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# Attempting to use mkl_fft (faster FFT library for Intel CPUs). Fallback is np
try:
    import mkl_fft as m  # type: ignore

    fft2 = m.fft2
    ifft2 = m.ifft2
except (ModuleNotFoundError, ImportError):
    fft2 = np.fft.fft2
    ifft2 = np.fft.ifft2
finally:
    fftshift = np.fft.fftshift
    ifftshift = np.fft.ifftshift

def np_ifft(kspace: np.ndarray, out: np.ndarray):
    """Perform inverse FFT function (kspace to [magnitude] image).

    Performs iFFT on the input data and updates the display variables for
    the image domain (magnitude) image and the kspace as well.

    Parameters
    ----------
        kspace (np.ndarray): Complex kspace ndarray
        out (np.ndarray): Array to store values
    """
    np.absolute(fftshift(ifft2(ifftshift(kspace))), out=out)

# [START instantiate_dag]
with DAG(
    dag_id='dag_reco_v01',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
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
    # [END instantiate_dag]

    @task()
    def list_directory(directory: str):
        """
        Task to list files in a directory.
        """
        files = os.listdir(directory)
        print(f"Files in {directory}: {files}")
        return files
    
    @task()
    def create_directories(*directories: str):
        """
        Task to create necessary directories.
        """
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            else:
                print(f"Directory already exists: {directory}")

    @task()
    def read_file(file_path: str, file_name: str):
        """
        Task to read the uploaded file.
        """
        input_file_path = f"{file_path}/{file_name}"
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"File not found: {input_file_path}")
        
        print(f"Verified file: {input_file_path}")
        return input_file_path

    @task()
    def extract_zip_file(input_file_path: str, temporary_path: str):
        """
        Task to extract the zip file.
        """
        if is_zipfile(input_file_path):
            with ZipFile(input_file_path, 'r') as zip_ref:
                zip_ref.extractall(temporary_path)
                print(f"Extracted file: {input_file_path}")
            return temporary_path
        else:
            print(f"File is not a zip file: {input_file_path}")
            return input_file_path

    @task(multiple_outputs=True)
    def reco_via_fft(input_file_path: str, output_path: str):
        """
        #### Transform task
        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        """

        record_id = "test_001"

        print(f"Loading K-Space from {input_file_path}")

        kspacedata = np.load(input_file_path)

        print("K-Space")
        print(kspacedata.shape)
        print(kspacedata[0][0])

        print("A")

        img = np.zeros_like(kspacedata, dtype=np.float32)

        print("B")

        np_ifft(kspacedata, img)

        print("C")


        # ################################################################
        # # Store DICOM
        # ################################################################

        img16 = img.astype(np.float16)

        print("Setting file meta information...")
        # Populate required values for file meta information

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

        dicom_dataset.Rows = img16.shape[0]
        dicom_dataset.Columns = img16.shape[1]
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
        dicom_dataset.PixelData = img16.tobytes()

        # Save as DICOM
        print("Saving file...")
        print(dicom_dataset)
        # Option 1: save to disk

        file_name = f"record-{record_id}.dcm"
        file_path = f"{output_path}/{record_id}/{file_name}"

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path)) # Ensure the directory exists

        print(f"Saving DICOM file to {file_path}")

        # Save the dataset to a DICOM file
        dicom_dataset.save_as(file_path)

        # # Convert from dicom to dicom with gdcmconv to add P10 header -> temporary fix
        # cmd = f"gdcmconv -C {file_path} {file_path}"
        # os.system(cmd)  # noqa: S605  # returns the exit code in unix

        # Option 2: save to orthanc
        # client = DICOMwebClient(url="http://scanhub_new-orthanc-1:8042/dicom-web")
        # client.store_instances(datasets=[ds])
        print("File saved.")

        # # Update exam manager with new record URL
        # requests.put(
        #     f"http://{EXAM_MANAGER_URI}/api/v1/exam/record/{record_id}/",
        #     json={
        #         "data_path": f"http://localhost:8080/api/v1/workflow/image/{record_id}/",
        #         "comment": "Created DICOM",
        #     },
        #     timeout=60,
        # )

        return {
            'file_path': file_path,
            'record_id': record_id
        }


    # Define the file paths
    data_lake_path = os.getenv('DATA_LAKE_DIRECTORY', '/opt/airflow/data_lake')
    INPUT_DIR = '{{ dag_run.conf["directory"] }}'
    INPUT_FILE = '{{ dag_run.conf["file_name"] }}'
    WORKFLOW_MANAGER_ENDPOINT = '{{ dag_run.conf["workflow_manager_endpoint"] }}'
    USER_TOKEN = '{{ dag_run.conf["user_token"] }}'

    input_path = f"{data_lake_path}{INPUT_DIR}"
    temporary_path = f"{data_lake_path}/temp/dag_process_uploaded_file"
    output_path = f"{data_lake_path}/results/dag_process_uploaded_file"

    # Define the task dependencies
    files = list_directory(input_path)
    create_dirs = create_directories(temporary_path, output_path)
    input_file_path = read_file(input_path, INPUT_FILE)
    extracted_path = extract_zip_file(input_file_path, temporary_path)
    results = reco_via_fft(extracted_path, output_path)
    # result_file = save_results(output_path, image_file)
    # result_file = save_results(output_path, image_file)
    # notify_workflow_manager_task = notify_workflow_manager(WORKFLOW_MANAGER_ENDPOINT, result_file, USER_TOKEN)
