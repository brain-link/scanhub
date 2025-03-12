# examples/simulate_scan.py

import asyncio
from device_sdk import Client

async def perform_scan(client, deviceTask):
    # Simulates a scanning process by sending status updates.
    # header_xml = ET.fromstring(header_xml_str)
    print(deviceTask)

    if "record_id" not in deviceTask:
        client.send_error_status("Missing record_id in deviceTask")

    await client.send_init_status()
    print("Initialization status sent.")

    for percentage in [0, 25, 50, 75, 100]:
        await asyncio.sleep(2)
        await client.send_scanning_status(percentage, 
                                          record_id=deviceTask["record_id"], 
                                          user_access_token=deviceTask["user_access_token"])
        print(f"Scanning progress: {percentage}%")

    await client.send_ready_status()
    print("Ready status sent.")

async def feedback_handler(message):
    print(f"Server Feedback: {message}")

async def error_handler(message):
    print(f"Server Error: {message}")


async def main():
    client = Client(
        websocket_uri="ws://localhost:8002/api/v1/device/ws2",  # Replace with actual WebSocket URI
        device_id="Device123",  # Unique device ID
        name="Device001",
        manufacturer="AcmeCorp",
        modality="XRAY",
        status="init",
        site="MainHospital",
        ip_address="192.168.1.100"
    )

    client.set_feedback_handler(feedback_handler)
    client.set_error_handler(error_handler)

    client.set_scan_callback(lambda deviceTask: perform_scan(client, deviceTask))

    await client.start()
    print("Client started and waiting for commands from the server.")
    await client.send_ready_status()

    try:
        while True:
            await asyncio.sleep(3)
    except KeyboardInterrupt:
        print("Shutting down client.")
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
