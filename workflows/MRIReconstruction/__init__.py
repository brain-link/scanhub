import logging

import azure.functions as func


def main(mrirawblob: func.InputStream):
    logging.info(f"Python MRI Reco blob trigger function processed blob \n"
                 f"Name: {mrirawblob.name}\n"
                 f"Blob Size: {mrirawblob.length} bytes")
