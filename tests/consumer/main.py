from kafka import KafkaConsumer
import json

from TimestampEvent import TimestampEvent

consumer = KafkaConsumer(             
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')), 
                        bootstrap_servers=['localhost:9092'],
                        auto_offset_reset='earliest')
consumer.subscribe(['timestamp'])
while True:
    try:
        records = consumer.poll(timeout_ms=1000)
        

        for topic_data, consumer_records in records.items():
            for consumer_record in consumer_records:
                timestampEvent = TimestampEvent(**(consumer_record.value))
                print("Received: " + timestampEvent.timestamp)
        continue
    except Exception as ex:
        print(f'Exception: {ex}')
        continue
