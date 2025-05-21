# examples/simulate_scan.py

import asyncio
import time

from device_sdk import Client
# from device_sdk import fill_mrd_template


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

    # TODO call function to perform scan
    # TODO if result not in MRD format call fill_mrd_template with raw data
    # TODO send MRD result with the client to Scanhub

    await client.send_ready_status()
    print("Ready status sent.")

async def feedback_handler(message):
    print(f"Server Feedback: {message}")

async def error_handler(message):
    print(f"Server Error: {message}")


async def main():
    # Replace the parameters for each particular device!
    client = Client(
        websocket_uri="wss://localhost/api/v1/device/ws",
        device_id="281cf4a3-727f-417e-878a-5017a914b002",
        device_token="3c97da12e5486b8bf48825d21403546703aac006e6dca46d7beab8d367499040a97353bb101ecf8a0b4e9dfd5ea16b2ac4b3f717fae45095aef32daf527538c8483dc6a1909d3327031803daa858c7ae5042de556b8ae0939f13f1d7b42ec0085829b79185f23317a140c75b4df36da2fc0d330d62b05d3abb0131c274dfde6517a5d425b76701aac7cda99af31d360f01c90ad90c4bfa0b26c22ad8cbefab0ddc3a237c62194bdb41425a1ae2f154e8217c3ff1359d9c835eed3d9f033d243f6513582d8ca0dfc5f87f895afb702ca199dabe5aab408773d642f48147042c62185e7d593e154b70b67b8109d09fd2f1356bfc251ec44e179fc69940346b24a94da6a9509730fa746369aace6b59b60b0deaacac4f9fe27ce8664490f48ebe2c96f50e9da26b7b00a82b321d5ba660eb82e79cbcb984f8dfdcfd82dd7baa110d2e7345057f0aee3017b859c1395b95937776f07a83be5fc3e8b73de1c859157fc1c8c06ad0a699b21f3a0ecda79ee32f005972a0d42f5688c1bdd8d41c62694320f912448e07e9482f0cc0cb4dc792ef016f870b0cce7444f2371a670761137190fb21b52286e3d8d427a0e1f19d0607eb294d0bcc466d85e22505736d5ca0c61064799b486f4dab08d696532e0a6aaef6e3b1a01a1a7ad0a026c436d5b690193dca28499022f9e36f593cdfc85134e91b73da827b33e39d07359c639d691056f4706b9e05bd08106defc12130e7b085b156ffb287b7d9822316f41bc903ef3e5ce22f67e31781da40472d55467fd88d9cae5fbfb73efa4c8046e46a6bfc818cd9b984bcc2a19f5dd9cb8b8d9aafe596d6bcefd30e26ef5e816046084aec75247188c870512daefae6631f80f2617898e07ede4e36fe127be6d955baa5cc7672e71ca2a7926a85db657ae5f4fe0885d2d51aa37750d8c7d5c982705cc9eb57b272ffb8d6551ed73383ff9f08924da73c0eff81b95ec28112c54eb047f6c4cd64f5be114a493a6dfad8531853a6b293b393dfe323f2169a08d4f0d09e83ce6b43416d061a3ba48c04d59611cbd79f365bb60c4b8357ccbc1c95401ffa26fc7f6a61d759dc10c88cf8bba5dc1f18be28224968676f0dc6c8aec7bd8c64212dae7be409c433c61d7165ae1d6b19c995389a59eb5fddc1fee81f33f94c5b9836b9a0602aaf88ecf1d333c5c772fc8b4ae2b5ed67dd4ea4e2788ad69227728cd13750d555d3f4500cb2938feed1881c36d6eb4b04a9c85d6026f4ea2b31165f577f9f686fbd28458783180ae094d869ce70feb806b4a10ff70a9b77a9ef43dafe3b8389e773be78733981148d01e9327675df6b207453777bc54411818fd2f05aac2d792fd55e148c23a1dd5934a6b25dc76a999d7ba2650c9eee1a763028dff340274ff5ce64714c215477612763d6a390c2720ec526d6c4858e9ef407edcc424cd0",
        name="Device001",
        manufacturer="AcmeCorp",
        modality="XRAY",
        status="init",
        site="MainHospital",
        ip_address="192.168.1.100",
        ca_file="../../../secrets/certificate.pem"
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
