# [START import_module]
import os
import json
import numpy as np
import pydicom
import pydicom._storage_sopclass_uids


from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.models import Variable

from pydantic import BaseModel, StrictStr
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

# [START instantiate_dag]
@dag(dag_id='dag_reco_v01', 
     default_args=default_args, 
     start_date=datetime(2025, 1, 1), 
     schedule_interval=None,
     catchup=False,
     tags=['scanhub', 'reconstruction'])
def cartesian_reco_etl():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    # [END instantiate_dag]

    # [START extract]
    @task()
    def extract():
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
        """
        # Get env just for demo purposes
        env = Variable.get("env")
        print(f"Running in {env} environment")

        # Generate random data
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict

    # [END extract]

    # [START transform]
    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        #### Transform task
        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        """
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        # log.info("starting cartesian reco with message: %s", message)
        # reco_job = RecoJob(**(message.value))
        # log.info("reco_job.input: %s", reco_job.input)

        # app_filename = f"/app/data_lake/{reco_job.input}"

        # log.info("Loading K-Space from %s", app_filename)

        # kspacedata = np.load(app_filename)

        # log.info("K-Space")
        # log.info(kspacedata.shape)
        # log.info(kspacedata[0][0])

        # img = np.zeros_like(kspacedata, dtype=np.float32)

        # np_ifft(kspacedata, img)

        return {"total_order_value": total_order_value}

    # [END transform]

    # [START load]
    @task()
    def load(total_order_value: float):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        """

        print(f"Total order value is: {total_order_value:.2f}")

        # ################################################################
        # # Store DICOM
        # ################################################################

        # img16 = img.astype(np.float16)

        # log.info("Setting file meta information...")
        # # Populate required values for file meta information

        # meta = pydicom.Dataset()
        # # pylint: disable=protected-access
        # meta.FileMetaInformationGroupLength = 212
        # meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
        # meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        # meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
        # meta.SourceApplicationEntityTitle = "BRAIN-LINK"

        # dicom_dataset = Dataset()
        # dicom_dataset.file_meta = meta  # type: ignore

        # dicom_dataset.is_little_endian = True
        # dicom_dataset.is_implicit_VR = False

        # # pylint: disable=protected-access
        # dicom_dataset.SOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
        # dicom_dataset.PatientName = "Max^Mustermann"
        # dicom_dataset.PatientID = "123456"

        # dicom_dataset.Modality = "MR"
        # dicom_dataset.SeriesInstanceUID = pydicom.uid.generate_uid()
        # dicom_dataset.StudyID = pydicom.uid.generate_uid()
        # dicom_dataset.SOPInstanceUID = pydicom.uid.generate_uid()
        # dicom_dataset.StudyInstanceUID = pydicom.uid.generate_uid()
        # dicom_dataset.FrameOfReferenceUID = pydicom.uid.generate_uid()

        # dicom_dataset.BitsStored = 16
        # dicom_dataset.BitsAllocated = 16
        # dicom_dataset.SamplesPerPixel = 1
        # dicom_dataset.HighBit = 15

        # dicom_dataset.ImagesInAcquisition = "1"

        # dicom_dataset.Rows = img16.shape[0]
        # dicom_dataset.Columns = img16.shape[1]
        # dicom_dataset.InstanceNumber = 1

        # dicom_dataset.ImagePositionPatient = r"0\0\1"
        # dicom_dataset.ImageOrientationPatient = r"1\0\0\0\-1\0"
        # dicom_dataset.ImageType = r"ORIGINAL\PRIMARY\AXIAL"

        # dicom_dataset.RescaleIntercept = "0"
        # dicom_dataset.RescaleSlope = "1"
        # dicom_dataset.PixelSpacing = r"1\1"
        # dicom_dataset.PhotometricInterpretation = "MONOCHROME2"
        # dicom_dataset.PixelRepresentation = 1

        # pydicom.dataset.validate_file_meta(dicom_dataset.file_meta, enforce_standard=True)

        # log.info("Setting pixel data...")
        # dicom_dataset.PixelData = img16.tobytes()

        # # Save as DICOM
        # log.info("Saving file...")
        # log.info(dicom_dataset)
        # # Option 1: save to disk

        # file_name = f"record-{reco_job.record_id}.dcm"
        # file_path = f"/app/data_lake/records/{reco_job.record_id}/{file_name}"
        # dicom_dataset.save_as(file_path)

        # # Convert from dicom to dicom with gdcmconv to add P10 header -> temporary fix
        # cmd = f"gdcmconv -C {file_path} {file_path}"
        # os.system(cmd)  # noqa: S605  # returns the exit code in unix

        # # Option 2: save to orthanc
        # # client = DICOMwebClient(url="http://scanhub_new-orthanc-1:8042/dicom-web")
        # # client.store_instances(datasets=[ds])
        # log.info("File saved.")

        # # Update exam manager with new record URL
        # requests.put(
        #     f"http://{EXAM_MANAGER_URI}/api/v1/exam/record/{reco_job.record_id}/",
        #     json={
        #         "data_path": f"http://localhost:8080/api/v1/workflow/image/{reco_job.record_id}/",
        #         "comment": "Created DICOM",
        #     },
        #     timeout=60,
        # )

    # [END load]

    # [START main_flow]
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])
    # [END main_flow]

# [START dag_invocation]
reco_dag = cartesian_reco_etl()
# [END dag_invocation]