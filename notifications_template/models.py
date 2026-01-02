from sqlalchemy import Column,String,Integer,Boolean
from core.database import Base_model


class Templates(Base_model):
    __tablename__="templates"

    id=Column(Integer,primary_key=True,autoincrement="auto")
    template_key=Column(String(255),unique=True)
    subject=Column(String(255))
    temp_text=Column(String(5000))


class SMS(Base_model):
    __tablename__="sms"

    id=Column(Integer,primary_key=True,autoincrement="auto")
    template_key=Column(String(255),unique=True)
    subject=Column(String(255))
    temp_text=Column(String(5000))