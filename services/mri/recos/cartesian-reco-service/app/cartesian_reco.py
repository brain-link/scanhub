# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Cartesian reco file for the MRI cartesian reco service."""

import logging
from typing import Any, Set

import numpy as np
import pydicom
import pydicom._storage_sopclass_uids
from pydicom.dataset import Dataset
from scanhub import RecoJob

# initialize logger
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)

# Attempting to use mkl_fft (faster FFT library for Intel CPUs). Fallback is np
try:
    import mkl_fft as m

    fft2 = m.fft2
    ifft2 = m.ifft2
except (ModuleNotFoundError, ImportError):
    fft2 = np.fft.fft2
    ifft2 = np.fft.ifft2
finally:
    fftshift = np.fft.fftshift
    ifftshift = np.fft.ifftshift


def np_ifft(kspace: np.ndarray, out: np.ndarray):
    """Performs inverse FFT function (kspace to [magnitude] image)

    Performs iFFT on the input data and updates the display variables for
    the image domain (magnitude) image and the kspace as well.

    Parameters:
        kspace (np.ndarray): Complex kspace ndarray
        out (np.ndarray): Array to store values
    """
    np.absolute(fftshift(ifft2(ifftshift(kspace))), out=out)


def cartesian_reco(message: Any) -> None:
    log.info(f"starting cartesian reco with message: {message}")
    reco_job = RecoJob(**(message.value))
    log.info(f"reco_job.input: {reco_job.input}")

    app_filename = f"/app/data_lake/{reco_job.input}"

    log.info(f"Loading K-Space from {app_filename}")

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
    meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    ds = Dataset()
    ds.file_meta = meta

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.SOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    ds.PatientName = "Max^Mustermann"
    ds.PatientID = "123456"

    ds.Modality = "MR"
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.StudyID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.SOPClassUID = "RT Image Storage"
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.FrameOfReferenceUID = pydicom.uid.generate_uid()

    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SamplesPerPixel = 1
    ds.HighBit = 15

    ds.ImagesInAcquisition = "1"

    ds.Rows = img16.shape[0]
    ds.Columns = img16.shape[1]
    ds.InstanceNumber = 1

    ds.ImagePositionPatient = r"0\0\1"
    ds.ImageOrientationPatient = r"1\0\0\0\-1\0"
    ds.ImageType = r"ORIGINAL\PRIMARY\AXIAL"

    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"
    ds.PixelSpacing = r"1\1"
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 1

    pydicom.dataset.validate_file_meta(ds.file_meta, enforce_standard=True)

    log.info("Setting pixel data...")
    ds.PixelData = img16.tobytes()

    # Save as DICOM
    log.info("Saving file...")
    log.info(ds)
    # Option 1: save to disk

    file_name = f"{reco_job.reco_id}.dcm"

    ds.save_as(f"/app/data_lake/records/{reco_job.record_id}/{file_name}")

    # Option 2: save to orthanc
    # client = DICOMwebClient(url="http://scanhub_new-orthanc-1:8042/dicom-web")
    # client.store_instances(datasets=[ds])
    log.info("File saved.")

    # TBD Call topic from a stack or fixed topic
