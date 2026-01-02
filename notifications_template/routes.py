from fastapi import APIRouter,Response,Body,Depends
from core.database import get_db
from sqlalchemy.orm import Session
from producers.producer_file import produce_kafka_message
from notifications_template import schemas
from jinja2 import Template
from notifications_template.models import Templates
from notifications_template.schemas import NotificationRequest
router=APIRouter(prefix="/notification",tags=["notification"])

@router.get("/health")
def get_health():
    return Response(content="Health is Fine",status_code=200)

@router.get("/fetch_user/{user_id}")
def fetch_user_data(user_id:int):
    return {"user_id":"id","username":"username","email":"hritikchoukikarwork24@gmail.com","type":{'sms':True,'email':True}}

@router.post("/send_notfication")
def send_notification(data:NotificationRequest,db:Session=Depends(get_db)): #user_id,user_name,to,type,template_type

    email_template=db.query(Templates).filter(Templates.template_key==data["template_type"]).first()


    data_=email_template.temp_text 
    template=Template(data_)
     
    rendered_text = template.render(user=data["user_name"])

    data["body"]=rendered_text

    data_=email_template.subject 
    template=Template(data_)
     
    rendered_text = template.render(user=data["user_name"])
    data["subject"]=rendered_text
    temp=produce_kafka_message(data)
    if temp:
        return {"Notification":"sent"}
    else:
        return {"Not-Notification":"Not sent"}
    
        