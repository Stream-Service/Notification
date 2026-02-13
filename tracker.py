from confluent_kafka import Consumer, Producer
import json
import smtplib
from email.message import EmailMessage
import threading
import socket
from core.config import setting

# --- CONFIGURATION ---
 
KAFKA_TOPIC = "email"
KAFKA_DLQ_TOPIC = "email_dlq"  # <--- New Dead Letter Queue Topic

# GMAIL CONFIGURATION
SENDER_EMAIL = "hritikchoukikarwork24@gmail.com"

SENDER_PASSWORD=setting.email
 
# Consumer Config
consumer_config = {
    "bootstrap.servers": setting.KAFKA_BOOTSTRAP_SERVERS,
    "group.id": "email_service_group",
    "auto.offset.reset": "earliest"
}

# Producer Config (For the Dead Letter Queue)
producer_config = {
    "bootstrap.servers": setting.KAFKA_BOOTSTRAP_SERVERS,
    "client.id": socket.gethostname()
}

def send_email_via_gmail(email_data):
    """
    Sends email using Gmail SMTP.
    Raises an exception if sending fails so the main loop knows to use DLQ.
    """
    msg = EmailMessage()
    msg['Subject'] = email_data.get("subject", "No Subject")
    msg['From'] = SENDER_EMAIL
    msg['To'] = email_data.get("to")
    msg.set_content(email_data.get("body", ""))

    # We do NOT use try/except here. We let the error bubble up 
    # so the consumer loop can catch it and send to DLQ.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)
        print(f"✅ Email sent successfully to {email_data.get('to')}")

def delivery_report(err, msg):
    """ Callback called once message delivered to DLQ or failed """
    if err is not None:
        print(f"❌ Failed to deliver message to DLQ: {err}")
    else:
        print(f"⚠️  Moved failed message to DLQ: {msg.topic()}")

def consumerloop(): 
    consumer = Consumer(consumer_config)
    consumer.subscribe([KAFKA_TOPIC])
    
    # Initialize Producer for DLQ
    producer = Producer(producer_config)

    print(f"Consumer running. Subscribed to: '{KAFKA_TOPIC}'. DLQ: '{KAFKA_DLQ_TOPIC}'")
    
    try:
        while True:
            msg = consumer.poll(1.0) 
            
            if msg is None: 
                continue 
            if msg.error(): 
                print(f"Consumer Error: {msg.error()}") 
                continue 
            
            # Get raw value for DLQ in case of JSON error
            raw_value = msg.value()
            
            try:
                # 1. Try to Decode JSON
                value_str = raw_value.decode("utf-8")
                email_data = json.loads(value_str) 
                
                # 2. Check for required fields
                if not email_data.get("to"):
                    raise ValueError("Missing 'to' field in email data")

                print(f"📩 Processing: {email_data.get('to')}") 
                
                # 3. Try to Send Email
                send_email_via_gmail(email_data)

            except (json.JSONDecodeError, ValueError, smtplib.SMTPException, Exception) as e:
                # --- DEAD LETTER QUEUE LOGIC ---
                print(f"❌ Error processing message: {e}")
                
                # Prepare the payload for the DLQ
                # We wrap the original message with the error reason
                dlq_payload = {
                    "original_message": value_str if 'value_str' in locals() else str(raw_value),
                    "error_reason": str(e),
                    "failed_at_topic": KAFKA_TOPIC
                }
                
                # Send to DLQ Topic
                producer.produce(
                    KAFKA_DLQ_TOPIC, 
                    json.dumps(dlq_payload).encode('utf-8'), 
                    callback=delivery_report
                )
                producer.poll(0) # Trigger the callback

    except KeyboardInterrupt:
        pass
    finally:
        print("Closing consumer and flushing producer...")
        consumer.close()
        producer.flush()

def start_consumer(): 
    thread = threading.Thread(target=consumerloop, daemon=True) 
    thread.start()
    return thread

if __name__ == "__main__":
    consumerloop()