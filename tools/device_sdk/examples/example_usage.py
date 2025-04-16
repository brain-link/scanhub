# examples/simulate_scan.py

import asyncio
import time

from device_sdk import Client

async def perform_scan(client, deviceTask):
    # Simulates a scanning process by sending status updates.
    # header_xml = ET.fromstring(header_xml_str)
    print(deviceTask)

    if "record_id" not in deviceTask:
        client.send_error_message("Missing record_id in deviceTask")

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
        websocket_uri="ws://localhost:8080/api/v1/device/ws",  # Replace with actual WebSocket URI
        device_id="41ea8b66-09ea-4442-bb47-71419fc0689e",
        device_token="2ee16286bbcccd8e8c3fd5010a22eb5d65292af01afdd1805b8a026c45622a4f728b69ef14942c7a2a3391c57aa1ebc4afe5ae0548eb2022ce5155262b22a5d9586c183234a7f9c1e7f957f77444666c660822df338718ea19a5e4aac97eb2391ca0d81eab66477ecb9a1a68a734f579b555afe9981428c754388f0e4b355e41656aa9edbe8645d6e561fab5b7d83b2c03da7dcddd745552e4381b76005d067b5f4a0670586226abeb5e251f040fb4897bdb3baf2fc748c477739441302a953d6d28abe808690bbde1d66721a05c03519f4b6cf3ac935c5c98c69006a2e1f6e78ac7afc07929a29224cacd075ebb9c88a849d2a7e6dac028a805e6fc3481d5b4cf420c6988b5725c6c1789453f5358f12ba7ac5997934ed5e50b27d5af2e5b536569aa5fdf0c85cd04d9a8ff744c0ab79b271bd8d64343f1c8ac3c7c2afaa0731ebfc45b796a3854a7502f4c5bfd15d63654d19b70f66478e888672aba59373fef47cf05fd26362b1b5e1b2214822165f96cddc73fbf5b52d5203c1046fc3205c91566aeb79e6d2c51a737e443e0ca9ad8e5e5627767ea65ea661c4f40ef39cfd90d04156596422ae7957ef1c9056a6980b9f0def0ef5150d24054b564280890c9d95ad7d03d0c6db165a837c23715e925cbd27abcc37d1958b1caeaad68e94963d4a5c6262d9078716b2486b6e64ff0d35f941c1a93c0839930019520dbab22338c7186a2ef9d7ec57fb0bc4fb59564cc24c7e42243b59f2f500885ec092830ba62fcf2d3502137b9ff28695a387effc494a65f0faa600130deb16a617387bf86065e8d6ee05bfd852a2cd84dad539d5da3ad37def854dbe9b4a67bab190e9d71b8c68357eb47402c3e8db8f53c0ab2532e09f160bef0ef6c3fae04b2540f5dda8cd5c7524f723fdca0c4c880160cbec7e4d60296108590f81893813590b4d8ca86119c8e2e574babd4a0123cbd61408c21f53532a44cc6ebd570ff300734992a8411b521500be1374c58a48a3cba96cd79066f1de51bc09899d83d78429b0cae752eec07d33f4311384b53fde53675b5d583e96cac68e827e4b370225fa3aedb3c3e4aa84fb06f322aaacb99654caaaa99badea8f5d56f727ac43a206b0ae908eb96cccc29e64575e13b2ea604d294f16c610cad5c63a53da95eb0927fdaa24d0953460b34d28da97693ce9bcbca020bff9c03759e00a151b082696ae4d4485bd5a3879cc9ce84f5f3d7220493818be9f3d67c6e78cb4f6f29c307645ca571817f64027a37395e75484a669d9a323de02b3884b2afd2322c672751c54aa83ea7a5ab84a71557819339c3b558bd71af942944a75e58ed475ccba487f5e66df22244f256ca503f0b3215c98e03934e39a44bbf523da54627752dcad08301bbe0df8520a4bc87ac7749c57af59390b35819627f3e3d6c029060aa1e84127651b3",
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
