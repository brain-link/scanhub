# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, Image, InputContext, IOType, Operator, OutputContext


@md.input("image", Image, IOType.IN_MEMORY)
@md.output("image", DataPath, IOType.DISK)
# If `pip_packages` is specified, the definition will be aggregated with the package dependency list of other
# operators and the application in packaging time.
@md.env(pip_packages=["pydicom >= 2.3.1", "numpy >= 1.24.3"])
class DICOMOperator(Operator):
    """This Operator implements a MR DICOM image packager.

    It ingests a single input and provides a single output.
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        import numpy as np
        import pydicom
        import pydicom._storage_sopclass_uids
        from pydicom.dataset import Dataset

        img16 = op_input.get().astype(np.float16)

        # Populate required values for file meta information

        meta = pydicom.Dataset()
        # pylint: disable=protected-access
        meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
        meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

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
        dicom_dataset.SOPClassUID = "RT Image Storage"
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

        dicom_dataset.PixelData = img16.tobytes()

        # Save as DICOM

        output_folder = op_output.get().path
        output_path = output_folder / "final_output.dcm"

        dicom_dataset.save_as(output_path)
