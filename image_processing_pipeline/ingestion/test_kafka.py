from kafka import KafkaProducer

KAFKA_URL = "broker:29092"

try:
    producer = KafkaProducer(bootstrap_servers=KAFKA_URL)
    print("✅ Connected to Kafka!")
except Exception as e:
    print(f"❌ Failed to connect: {e}")