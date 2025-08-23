"""Example usage of the Device SDK for a simulated scanning process (cross-platform)."""
import asyncio
import os
import json
import signal
from pathlib import Path

from sdk.client import Client
from scanhub_libraries.models import AcquisitionPayload, DeviceDetails


async def perform_scan(client: Client, payload: AcquisitionPayload):
    """Simulate a scanning process by sending status updates and results."""
    print("Received acquisition request with task ID:", payload.id)

    # Update device status
    for percentage in [0, 25, 50, 75, 100]:
        await asyncio.sleep(1)
        await client.send_scanning_status(
            progress=percentage,
            task_id=str(payload.id),
            user_access_token=payload.access_token,
        )

    # Print device parameters obtained
    print("Retrieved device parameters dict:", payload.device_parameter)

    # Upload MRD result
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
        with open(credentials_path, "r", encoding="utf-8") as f:
            credentials = json.load(f)
    except FileNotFoundError:
        print(
            f"Credentials file not found at {credentials_path}. "
            "Please create a device first and save the credentials file."
        )
        return

    device_details = DeviceDetails(
        device_name="RandomDataSimulator",
        serial_number="v1.0",
        manufacturer="BrainLink",
        modality="MRI",
        site="Berlin",
        parameter={
            "larmor_frequency": 2.025e6,
        },
    )

    client = Client(
        websocket_uri="wss://localhost:8443/api/v1/device/ws",
        device_id=credentials.get("device_id"),
        device_token=credentials.get("device_token"),
        ca_file="../../secrets/certificate.pem",
        device_details=device_details,
    )

    client.set_feedback_handler(feedback_handler)
    client.set_error_handler(error_handler)
    client.set_scan_callback(lambda deviceTask: perform_scan(client, deviceTask))

    await client.start()
    print("Client started and waiting for commands from the server.")
    await client.send_ready_status()

    # --- Cross-platform graceful shutdown ---
    stop_event = asyncio.Event()

    def shutdown():
        # idempotent; safe to call multiple times
        if not stop_event.is_set():
            stop_event.set()

    try:
        loop = asyncio.get_running_loop()
        # Works on Unix; raises NotImplementedError on Windows (Proactor loop)
        loop.add_signal_handler(signal.SIGINT, shutdown)
        loop.add_signal_handler(signal.SIGTERM, shutdown)
        await stop_event.wait()
    except (NotImplementedError, RuntimeError):
        # Fallback for Windows/Proactor: rely on KeyboardInterrupt (Ctrl+C)
        try:
            while not stop_event.is_set():
                await asyncio.sleep(3600)
        except KeyboardInterrupt:
            shutdown()

    print("\nStopping client...")
    try:
        await client.stop()
    except Exception as e:
        print(f"Error while stopping client: {e}")


if __name__ == "__main__":
    asyncio.run(main())