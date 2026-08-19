"""Example usage of the Device SDK for a simulated scanning process."""
import asyncio

from sdk.client import Client
from scanhub_libraries.models import AcquisitionPayload, DeviceDetails, CalibrationType
import os
import json
import logging
from pathlib import Path
import datetime

logging.basicConfig(level=logging.INFO)

WSS_ENDPOINT = "wss://localhost:8443/api/v1/device/ws"
EXAMPLE_DIR = Path(__file__).resolve().parent

# Download an ISMRMRD file from zenodo if it not already exists
if not (EXAMPLE_DIR / "LLR").exists():
    import signal
    import zenodo_get
    import zipfile

    # zenodo_get installs its own SIGINT handler on import, which hijacks Ctrl+C
    # for the whole process even after the download above is done. Restore the
    # default handler so Ctrl+C behaves normally for the rest of the script.
    signal.signal(signal.SIGINT, signal.default_int_handler)

    print("Downloading example data...")
    zenodo_get.download(
        record="19661402",
        retry_attempts=5,
        output_dir=EXAMPLE_DIR,
        file_glob=("LLR.zip",),
        access_token=os.environ.get("ZENODO_TOKEN"),
    )
    with zipfile.ZipFile(EXAMPLE_DIR / Path("LLR.zip"), "r") as zip_ref:
        zip_ref.extractall(EXAMPLE_DIR)


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
        file_path=EXAMPLE_DIR / "LLR/noise_corr_off/9003/IR_T1w_TSE_PF.h5",
        name=file_name,
        parameter=payload.device_parameter,
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
    client.set_scan_callback(lambda deviceTask: perform_scan(client, deviceTask))


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
