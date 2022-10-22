import os
import httpx

DEVICE_SERVICE_HOST_URL = 'http://localhost:8002/api/v1/devices/'

def is_cast_present(cast_id: int):
    url = os.environ.get('DEVICE_SERVICE_HOST_URL') or DEVICE_SERVICE_HOST_URL
    r = httpx.get(f'{url}{cast_id}')
    return True if r.status_code == 200 else False