# https://blog.siliconvalve.com/2020/10/29/reading-and-writing-binary-files-with-python-with-azure-functions-input-and-output-bindings/
import logging
import azure.functions as func
import numpy as np
import io
from PIL import Image

from ..libraries.utils import storage_helpers
# from ..libraries.utils import processing

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


# def main(msg: func.QueueMessage, inputblob: func.InputStream, outputblob: func.Out[func.InputStream]) -> None:
#     logging.info('Python queue trigger function processed a queue item: %s',
#                  msg.get_body().decode('utf-8'))

#     blob_source_raw_name = msg.get_body().decode('utf-8')

#     buffer = inputblob.read()

#     kspacedata = np.load(io.BytesIO(buffer))

#     print("K-Space")
#     print(kspacedata.shape)
#     print(kspacedata[0][0])

#     img = np.zeros_like(kspacedata, dtype=np.float32)

#     np_ifft(kspacedata, img)

#     pil_img = Image.fromarray(img).convert(mode='L')
#     #pil_img.save("/tmp/mri.png")

#     # https://github.com/yokawasa/azure-functions-python-samples/tree/master/v2functions/blob-trigger-watermark-blob-out-binding

#     # Store final composite in a memory stream
#     img_byte_arr = io.BytesIO()
#     # Convert composite to RGB so we can save as JPEG
#     pil_img.convert('RGB').save(img_byte_arr, format='PNG')

#     # Set blob content from byte array in memory
#     blobout.set(img_byte_arr.getvalue())
    
#     logging.info(f"----- Cartesian reconstruction successful")




def main(msg: func.QueueMessage) -> None:
    
    file_name = ""

    try:

        file_name = msg.get_body().decode('utf-8')
        logging.info(f"### Processing queue item: {file_name}...")

        # # Getting settings
        # STORAGE_CONNECTION_STRING = os.getenv("QueueConnectionString")
        # CONTAINER_NAME = os.getenv("STORAGE_CONTAINER_NAME")
        # TABLE_NAME = os.getenv("STORAGE_TABLE_NAME")

        # # Updating status to new
        # storage_helpers.update_status(TABLE_NAME, file_name, 'new', STORAGE_CONNECTION_STRING)

        # # Getting file from storage
        # file_path = storage_helpers.download_blob(CONTAINER_NAME, file_name, STORAGE_CONNECTION_STRING)

        # if file_path != None:
        #     # Processing file
        #     processed_doc = processing.process_doc(file_path)
        #     # Saving processed file to storage
        #     if processed_doc != None:
        #         # Updating status to processed
        #         storage_helpers.update_status(TABLE_NAME, file_name, 'processed', STORAGE_CONNECTION_STRING)
        #         new_file_name = 'processed_' + file_name
        #         storage_helpers.upload_blob(CONTAINER_NAME, new_file_name, processed_doc, STORAGE_CONNECTION_STRING)
        #         # Updating status to done
        #         storage_helpers.update_status(TABLE_NAME, file_name, 'done', STORAGE_CONNECTION_STRING)
        #         # Deleting local copy
        #         os.remove(file_path)
        #         logging.info(f"Done processing {file_name}.")
        
        # else:
        #     logging.info(f"Did not perform any operation as there was an issue.")
        #     # Updating status to failed
        #     storage_helpers.update_status(TABLE_NAME, file_name, 'failed', STORAGE_CONNECTION_STRING)

    except Exception as e:
        logging.error(f"Error getting file name from msg: {e}")
