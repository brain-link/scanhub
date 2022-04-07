import logging

import azure.functions as func


# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )

# def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:

#         msg.set(func.QueueMessage(name))
#         # msg.set(name)

#         return func.HttpResponse(
#             f"Hello, {name}. This HTTP triggered function executed successfully.",
#             status_code=200
#         )
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )


# Test with
# curl --location --request POST 'http://localhost:80/api/TriggerProcessing' --header 'Content-Type: text/plain' --data-raw '{ "documentList": ["sample_file1.txt", "sample_file2.txt", "sample_file3.txt", "sample_file4.txt", "sample_file5.txt"] }'

def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        sender_ID = req_body.get('senderID')
        document_list = req_body.get('documentList')
    except ValueError:
        return func.HttpResponse(
             "Please pass a documentList parameter in the request body",
             status_code=400
        )
    
    if sender:
        logging.info(f"Received instruction from {sender_ID}.")

    if document_list:
        try:
            msg.set(document_list)
            return func.HttpResponse(
                "Processing started.",
                status_code=200
            )

        except Exception as e:
            return func.HttpResponse(
                f"Error: {e}",
                status_code=500
            )
