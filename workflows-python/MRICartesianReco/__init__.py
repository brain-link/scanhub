import logging
import azure.functions as func
import numpy as np
import io
from PIL import Image

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

    pil_img = Image.fromarray(img).convert(mode='L')
    #pil_img.save("/tmp/mri.png")

    # https://github.com/yokawasa/azure-functions-python-samples/tree/master/v2functions/blob-trigger-watermark-blob-out-binding

    # Store final composite in a memory stream
    img_byte_arr = io.BytesIO()
    # Convert composite to RGB so we can save as JPEG
    pil_img.convert('RGB').save(img_byte_arr, format='PNG')
    # pil_img.convert('RGB').save(img_byte_arr, format='jpg')

    # Set blob content from byte array in memory
    blobout.set(img_byte_arr.getvalue())
    
    logging.info(f"----- Cartesian reconstruction successful")