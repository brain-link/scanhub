import logging
import azure.functions as func
import numpy as np
import io
from PIL import Image

import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian
import pydicom._storage_sopclass_uids
from dicomweb_client.api import DICOMwebClient

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


def main(rawmriblob: func.InputStream, blobout: func.Out[func.InputStream]):
    logging.info(f"Python MRI Reco blob trigger function processed blob \n"
                 f"Name: {rawmriblob.name}\n"
                 f"Blob Size: {rawmriblob.length} bytes")
    
    buffer = rawmriblob.read()

    kspacedata = np.load(io.BytesIO(buffer))

    print("K-Space")
    print(kspacedata.shape)
    print(kspacedata[0][0])

    img = np.zeros_like(kspacedata, dtype=np.float32)

    np_ifft(kspacedata, img)

    # ################################################################
    # # Option 1: Create PNG
    # ################################################################

    # pil_img = Image.fromarray(img).convert(mode='L')
    # #pil_img.save("/tmp/mri.png")

    # # https://github.com/yokawasa/azure-functions-python-samples/tree/master/v2functions/blob-trigger-watermark-blob-out-binding

    # # Store final composite in a memory stream
    # img_byte_arr = io.BytesIO()
    # # Convert composite to RGB so we can save as JPEG
    # # pil_img.convert('RGB').save(img_byte_arr, format='PNG')
    # pil_img.convert('RGB').save(img_byte_arr, format='JPEG')

    # # Set blob content from byte array in memory
    # blobout.set(img_byte_arr.getvalue())
    
    ################################################################
    # Option 2: Store DICOM
    ################################################################

    img16 = img.astype(np.float16)

    print("Setting file meta information...")
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

    print("Setting pixel data...")
    ds.PixelData = img16.tobytes()

    out_byte_array = io.BytesIO()
    ds.save_as(out_byte_array) #ds.save_as(r"out.dcm")
    # Set blob content from byte array in memory
    blobout.set(out_byte_array.getvalue())
    
    client = DICOMwebClient(url="http://scanhub_new-orthanc-1:8042/dicom-web")
    client.store_instances(datasets=[ds])
    print("image sent")
    
    logging.info(f"----- Cartesian reconstruction successful")
