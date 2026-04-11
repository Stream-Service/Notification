from confluent_kafka import Producer
import json
from core.config import setting

producer_config= {
    "bootstrap.servers": setting.KAFKA_BOOTSTRAP_SERVERS,
    "message.max.bytes": 200000000
}


def delivery_report(err,msg):
    if err:
        print(f"Delivery Failed :{err}")
    else:
        print(f"Message dileverd { msg.value().decode("utf-8")}")

producer=Producer(producer_config)

def send_email_message(to, subject, body): 
    email_data = { "to": to, "subject": subject, "body": body } 

     
     

    value=json.dumps(email_data).encode("utf-8")

    producer.produce(topic="email",value=value,callback=delivery_report)

    producer.flush()


 


