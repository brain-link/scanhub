import logging

import azure.functions as func


def main(req: func.HttpRequest, controlQueue: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Acquisition HTTP trigger processed.')

    cmd = req.params.get('cmd')
    if not cmd:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            cmd = req_body.get('cmd')

    if cmd:
        # TBD done parse command to an existing enum, that only predefined commands are processed
        # cmd.set(func.QueueMessage(cmd))
        controlQueue.set(str(cmd))

        return func.HttpResponse(
            f"Received {cmd}.",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Acquisition HTTP triggered function but {cmd} has not been processed.",
            status_code=200
        )
