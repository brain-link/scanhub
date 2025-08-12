"""Example usage of the Device SDK for a simulated scanning process."""
import asyncio
import numpy as np

from sdk.client import Client
from scanhub_libraries.models import AcquisitionPayload
import os
import json
import signal
from pathlib import Path


async def perform_scan(client, payload: AcquisitionPayload):
    """Simulate a scanning process by sending status updates and results."""
    print("Received acquisition request with task ID: ", payload.id)

    for percentage in [0, 25, 50, 75, 100]:
        await asyncio.sleep(1)
        await client.send_scanning_status(
            progress=percentage,
            task_id=str(payload.id),
            user_access_token=payload.access_token,
        )

    # Create some random data to simulate scan results.
    # data = np.random.rand(42, 100, 120)
    # Submit the result, device status is set to READY.
    # await client.upload_result(
    #     result=data,
    #     task_id=str(payload.id),
    #     user_access_token=payload.access_token,
    # )

    # Get MRD file
    directory = Path(__file__).resolve().parent
    file_path = directory / "data.mrd"

    await client.upload_file_result(
        file_path=file_path,
        task_id=str(payload.id),
        user_access_token=payload.access_token,
    )

async def feedback_handler(message):
    print(f"Server Feedback: {message}")

async def error_handler(message):
    print(f"Server Error: {message}")


async def main():    
    credentials_path = os.path.join(os.path.dirname(__file__), "device_credentials.json")
    try:
        with open(credentials_path, "r") as f:
            credentials = json.load(f)
    except FileNotFoundError:
        print(f"Credentials file not found at {credentials_path}. Please create a device first and save credentials file.")
        return

    # Replace the parameters for each particular device!
    client = Client(
        websocket_uri="wss://localhost:8443/api/v1/device/ws",
        device_id=credentials.get("device_id"),
        device_token=credentials.get("device_token"),
        device_name="RandomDataSimulator",
        serial_number="v1.0",
        manufacturer="BrainLink",
        modality="MRI",
        site="Berlin",
        ca_file="../../secrets/certificate.pem"
    )

    client.set_feedback_handler(feedback_handler)
    client.set_error_handler(error_handler)
    client.set_scan_callback(lambda deviceTask: perform_scan(client, deviceTask))


    await client.start()
    print("Client started and waiting for commands from the server.")
    await client.send_ready_status()
    
    stop_event = asyncio.Event()
    def shutdown():
        stop_event.set()
        
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    await stop_event.wait()  # wait for signal
    
    print("\nStopping client...")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
