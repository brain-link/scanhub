
STEP 1: CREATE A TOPIC TO STORE YOUR EVENTS
opt/bitnami/kafka/bin/kafka-topics.sh --create --topic createStudyEvents --bootstrap-server localhost:9092
opt/bitnami/kafka/bin/kafka-topics.sh --create --topic deviceControlEvents --bootstrap-server localhost:9092

STEP 2: LIST AVAILABLE TOPICS
opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

opt/bitnami/kafka/bin/kafka-topics.sh --describe --topic createStudyEvent --bootstrap-server localhost:9092

STEP 3: WRITE SOME EVENTS INTO THE TOPIC
opt/bitnami/kafka/bin/kafka-console-producer.sh --topic createStudyEvent --bootstrap-server localhost:9092
This is my first event
This is my second event
You can stop the producer client with Ctrl-C at any time.

STEP 4: READ THE EVENTS
opt/bitnami/kafka/bin/kafka-console-consumer.sh --topic timestamp --from-beginning --bootstrap-server localhost:9092
