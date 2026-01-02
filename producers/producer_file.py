from kafka import KafkaProducer
from fastapi import HTTPException,status
import json
KAFKA_TOPIC='fastapi-topic'
PRODUCER_CLIENT_ID='fastapi-producer'
from core.config import setting


def serializer(message):
    return json.dumps(message).encode()

 
# Kafka Producer
try:
    producer = KafkaProducer(
        api_version=(2, 8, 0),
        bootstrap_servers='localhost:9092',
        value_serializer=serializer,
        client_id=PRODUCER_CLIENT_ID
    )
except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Kafka producer initialization failed: {str(e)}"
    )

def produce_kafka_message(message: dict):
    try:
        payload = {"message": message}
        producer.send(KAFKA_TOPIC, value=payload)
        producer.flush()
        return payload
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Kafka message production failed: {str(error)}"
        )
 