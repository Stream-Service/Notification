from confluent_kafka import Consumer
import json
import mailtrap as mt
from core.config import setting
import os
import threading

consumer_config= {
    "bootstrap.servers":"localhost:9092",
    "group.id":"email",
    "auto.offset.reset":"earliest"
}

 
 

client = mt.MailtrapClient(token=setting.api)
def send_email(email_data): 
    mail = mt.Mail( sender=mt.Address(email="hello@streaming.com", name="Notification Service"), to=[mt.Address(email=email_data["to"])], subject=email_data["subject"], text=email_data["body"], category="Notification" ) 
    response = client.send(mail) 
    print(f"Email sent via Mailtrap: {response}")
    print(response)

def consumerloop(): 
    
    consumer=Consumer(consumer_config)

    consumer.subscribe(["email"])

    print("consumer is running ans subscribeed to topic")
    while True:
        msg = consumer.poll(1.0) 
        if msg is None: 
            continue 
        if msg.error(): 
            print(f"GOT ERROR: {msg.error()}") 
            continue 
        value = msg.value().decode("utf-8") 
        email = json.loads(value) 
        print(f"Email received: {email}") 
        # Send email using Mailtrap 
        send_email(email)



def start_consumer(): # Run consumer loop in a separate thread 
    thread = threading.Thread(target=consumerloop, daemon=True) 
    thread.start()
