"""Example usage of the Device SDK for a simulated scanning process."""
import asyncio
import datetime
import json
import logging
import os
from pathlib import Path

from scanhub_libraries.models import AcquisitionPayload, DeviceDetails

from sdk.client import Client

logging.basicConfig(level=logging.INFO)

WSS_ENDPOINT = "wss://localhost:8443/api/v1/device/ws"

DATA_PATH = Path(__file__).resolve().parent / "data"
DATASET = "OSIIONE_Reference_System_Data_v1"
zip_file = (DATA_PATH / DATASET).with_suffix(".zip")

# Download an ISMRMRD file from zenodo if it not already exists
if not (DATA_PATH / DATASET).exists():
    import signal
    import zipfile

    import zenodo_get

    # zenodo_get installs its own SIGINT handler on import, which hijacks Ctrl+C
    # for the whole process even after the download above is done. Restore the
    # default handler so Ctrl+C behaves normally for the rest of the script.
    signal.signal(signal.SIGINT, signal.default_int_handler)

    print("Downloading example data...")
    zenodo_get.download(
        record="21807140",
        retry_attempts=5,
        output_dir=DATA_PATH,
        file_glob=zip_file.name,
    )
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(DATA_PATH)


async def perform_scan(client, payload: AcquisitionPayload):
    """Simulate a scanning process by sending status updates and results."""
    print("Received acquisition request with task ID: ", payload.id)
    # Print device parameters obtained
    print("Retrieved device parameters dict: ", payload.device_parameter)

    # Simulate some workload
    delay_per_step = 0.25
    for percentage in range(9):
        await asyncio.sleep(delay_per_step)
        await client.send_scanning_status(
            progress=(percentage+1)*10,
            task_id=str(payload.id),
            user_access_token=payload.access_token,
        )

    file_name = str(datetime.date.today()) + "_acquisition"

    await client.upload_file_result(
        file_path=DATA_PATH / DATASET / "2026-07-23-112655-tse_3d_PDw_100px_CaliberMRI" / "ismrmrd_data.h5",
        name=file_name,
        parameter=payload.device_parameter,
        task_id=str(payload.id),
        user_access_token=payload.access_token,
    )

async def feedback_handler(message):
    """Define callback action for server feedback."""
    print(f"Server Feedback: {message}")

async def error_handler(message):
    """Define callback action for server error."""
    print(f"Server Error: {message}")


async def main():
    """Define the main function."""
    credentials_path = os.path.join(os.path.dirname(__file__), "device_credentials.json")
    try:
        with open(credentials_path, "r") as f:
            credentials = json.load(f)
    except FileNotFoundError:
        print(f"Credentials file not found at {credentials_path}.\
            Please create a device first and save credentials file.")
        return

    device_details = DeviceDetails(
        device_name="SimpleSimulator",
        serial_number="v1.0",
        manufacturer="BrainLink",
        modality="MRI",
        site="Berlin",
        # The following dictonary can contain any parameter relevant for the acquisition process
        parameter={
            "larmor_frequency": 2.025e6,
        },
    )

    # Replace the parameters for each particular device!
    client = Client(
        websocket_uri=WSS_ENDPOINT,
        device_id=credentials.get("device_id"),
        device_token=credentials.get("device_token"),
        ca_file="../secrets/certificate.pem",
        device_details=device_details,
    )

    client.set_feedback_handler(feedback_handler)
    client.set_error_handler(error_handler)
    client.set_scan_callback(lambda device_task: perform_scan(client, device_task))


    await client.start()
    print("Client started and waiting for commands from the server.")

    stop_event = asyncio.Event()

    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        print("Cancellation requested, shutting down...")
    finally:
        await client.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt received.")
