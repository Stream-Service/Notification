from kafka import KafkaConsumer
import json
import requests
import logging
from fastapi import Request,HTTPException
from core.config import setting
from consumer.mailchimp import send_email_to_user # Gmail SMTP sender
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaEmailConsumer")
def consume_email_jobs():
    try:
        consumer = KafkaConsumer(
            "fastapi-topic",
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            group_id="email-consumer-group",
            auto_offset_reset="earliest",
            enable_auto_commit=True
        )
    except Exception as conn_error:
        logger.error(f"❌ Failed to connect to Kafka: {conn_error}")
        return

    try:
        for msg in consumer:
            job = msg.value
            logger.info(f"📨 Received job: {job}")

            try:
                if job.get("type") == "email":
                    recipient = job.get("to")
                    subject = job.get("subject")
                    body = job.get("body")

                    if not recipient or not subject or not body:
                        logger.error(f"❌ Missing required email fields: {job}")
                        continue

                    send_email_to_user(subject, body, recipient)
                    logger.info("✅ Email sent successfully.")

            except Exception as e:
                logger.error(f"❌ Error sending email: {e}")

    except KeyboardInterrupt:
        logger.info("🛑 Consumer interrupted.")
    finally:
        consumer.close()

                 

consume_email_jobs()