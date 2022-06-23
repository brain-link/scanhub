import logging

import azure.functions as func
import mimetypes

from ..libraries.utils import storage_helpers
from ..libraries.utils import processing

from PIL import Image

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Request Result HTTP trigger processed.')

    filename = req.params.get('filename')
    if not filename:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            filename = req_body.get('filename')

    # Getting settings
    STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://Storage:10000/devstoreaccount1;QueueEndpoint=http://Storage:10001/devstoreaccount1;TableEndpoint=http://Storage:10002/devstoreaccount1;" #os.getenv("STORAGE_CONNECTION_STRING")
    CONTAINER_NAME = "processed-mri" #os.getenv("STORAGE_CONTAINER_NAME")
    # CONTAINER_NAME = "processed-" + req.route_params.get('containername')
    message = f"Container: {CONTAINER_NAME}, File Name: {filename}"

    # Getting file from storage
    file_path = storage_helpers.download_blob(CONTAINER_NAME, filename, STORAGE_CONNECTION_STRING)

    print("#########")
    print(file_path)
    
    print(filename)

    #im = Image.open(file_path).convert("RGB")

    # with open(file_path, 'rb') as f:
    #     image_blob = f.read()

    # return func.HttpResponse(image_blob)
    # # path = 'static-file' # or other paths under `MyFunctionProj`
    # # filename = f"{path}/{name}"
    # # with open(filename, 'rb') as f:
    # #     mimetype = mimetypes.guess_type(filename)
    # #     return func.HttpResponse(f.read(), mimetype=mimetype[0])


    if file_path:
        with open(file_path, 'rb') as f:
            mimetype = mimetypes.guess_type(file_path)
            return func.HttpResponse(f.read(), mimetype=mimetype[0])
    else:
        return func.HttpResponse(
             "Please pass a filename on the query string or in the request body",
             status_code=400
        )