import logging

import azure.functions as func


import numpy as np



def main(rawmriblob: func.InputStream):
    logging.info(f"Python MRI Reco blob trigger function processed blob \n"
                 f"Name: {rawmriblob.name}\n"
                 f"Blob Size: {rawmriblob.length} bytes")

    buffer = rawmriblob.read()

    kspacedata = np.frombuffer(buffer, dtype=np.complex64)

    print(kspacedata)
    