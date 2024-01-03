# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Cartesian reco file for the MRI cartesian reco service."""

import logging
import os
from typing import Any

import numpy as np
import pydicom
import pydicom._storage_sopclass_uids
import requests
from pydantic import BaseModel, StrictStr
from pydicom.dataset import Dataset

# from scanhub import RecoJob # type: ignore


EXAM_MANAGER_URI = "host.docker.internal:8004"


class RecoJob(BaseModel):
    """RecoJob is a pydantic model for a reco job."""  # noqa: E501

    record_id: int
    input: StrictStr


# initialize logger
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

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


def cartesian_reco(message: Any) -> None:  # pylint: disable=too-many-statements
    """Run the cartesian reco.

    Parameters
    ----------
        message (Any): Message to run the cartesian reco
    """
    log.info("starting cartesian reco with message: %s", message)
    reco_job = RecoJob(**(message.value))
    log.info("reco_job.input: %s", reco_job.input)

    app_filename = f"/app/data_lake/{reco_job.input}"

    log.info("Loading K-Space from %s", app_filename)

    kspacedata = np.load(app_filename)

    log.info("K-Space")
    log.info(kspacedata.shape)
    log.info(kspacedata[0][0])

    img = np.zeros_like(kspacedata, dtype=np.float32)

    np_ifft(kspacedata, img)

    ################################################################
    # Store DICOM
    ################################################################

    img16 = img.astype(np.float16)

    log.info("Setting file meta information...")
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

    log.info("Setting pixel data...")
    dicom_dataset.PixelData = img16.tobytes()

    # Save as DICOM
    log.info("Saving file...")
    log.info(dicom_dataset)
    # Option 1: save to disk

    file_name = f"record-{reco_job.record_id}.dcm"
    file_path = f"/app/data_lake/records/{reco_job.record_id}/{file_name}"
    dicom_dataset.save_as(file_path)

    # Convert from dicom to dicom with gdcmconv to add P10 header -> temporary fix
    cmd = f"gdcmconv -C {file_path} {file_path}"
    os.system(cmd)  # noqa: S605  # returns the exit code in unix

    # Option 2: save to orthanc
    # client = DICOMwebClient(url="http://scanhub_new-orthanc-1:8042/dicom-web")
    # client.store_instances(datasets=[ds])
    log.info("File saved.")

    # Update exam manager with new record URL
    requests.put(
        f"http://{EXAM_MANAGER_URI}/api/v1/exam/record/{reco_job.record_id}/",
        json={
            "data_path": f"http://localhost:8080/api/v1/workflow/image/{reco_job.record_id}/",
            "comment": "Created DICOM",
        },
        timeout=60,
    )

    # TBD Call topic from a stack or fixed topic
