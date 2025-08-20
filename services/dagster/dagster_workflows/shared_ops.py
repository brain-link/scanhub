"""Definition of shared dagster operations."""
import json

import requests
from dagster import In, Nothing, OpExecutionContext, Out, op
from fastapi.encoders import jsonable_encoder
from scanhub_libraries.resources import SCANHUB_RESOURCE_KEY, JobConfigResource


@op(required_resource_keys={SCANHUB_RESOURCE_KEY}, ins={"after_save": In(Nothing)})
def notify_op(context: OpExecutionContext) -> None:
    """Notify backend about finished job using the callback url from the job configuration.

    This should always be the last step within the graph/job definition.
    Input needs to be None, if operation should be executed sequentially.
    """
    job_config: JobConfigResource = context.resources.job_config
    if job_config.callback_url and job_config.user_access_token:
        try:
            headers = {"Authorization": "Bearer " + job_config.user_access_token}
            with requests.post(job_config.callback_url, headers=headers, timeout=3) as callback_response:
                if callback_response.status_code != 200:
                    context.log.error(f"Callback failed with status code {callback_response.status_code}")
                else:
                    context.log.info("Callback successful")
        except Exception as e:
            context.log.error(f"Callback failed: {e}")


@op(required_resource_keys={SCANHUB_RESOURCE_KEY}, out=Out(Nothing))
def send_device_parameter_update(context: OpExecutionContext, data: dict) -> None:
    """Send an updated version of device parameters to device manager."""
    job_config: JobConfigResource = context.resources.job_config
    if (url := job_config.update_device_parameter_base_url) and job_config.user_access_token:
        try:
            if not "device_id" in data or not "parameter" in data:
                context.log.error("Invalid dictionary")
            device_id = data["device_id"]
            payload = json.dumps(data["parameter"], default=jsonable_encoder)
            headers = {"Authorization": "Bearer " + job_config.user_access_token}
            endpoint = url+device_id
            context.log.info(f"Device parameter update endpoint: {endpoint}")
            with requests.put(endpoint, data=payload, headers=headers, timeout=3) as callback_response:
                if callback_response.status_code != 200:
                    context.log.error(f"Callback failed with status code {callback_response.status_code}")
                else:
                    context.log.info(f"Callback successful. Updated device:\n{callback_response.json()}")
        except Exception as e:
            context.log.error(f"Callback failed: {e}")
