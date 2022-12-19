import json
from kafka import KafkaProducer
from datetime import datetime
from time import sleep

from AcquisitionEvent import AcquisitionEvent

try:
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x.__dict__).encode('utf-8'))
except Exception as ex:
    print(ex)

count = 0

while True:
    acquisitionEvent = AcquisitionEvent("MEAS_START" if count % 2 == 0 else "MEAS_STOP")
    print("Sending: " + acquisitionEvent.instruction)
    producer.send('acquisitionEvent', acquisitionEvent)
    count = count + 1
    sleep(10)
