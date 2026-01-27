from fastapi import FastAPI
from notifications_template.routes import router as noti_router
from database_template.template import router as db_router
from tracker import start_consumer
from producers.producer_admin import send_email_message
 

import asyncio 
from pydantic import BaseModel
 
 

# Define request body schema
class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

 
from core.database import engine,Base_model

Base_model.metadata.create_all(bind=engine)


app=FastAPI()
app.include_router(noti_router)
app.include_router(db_router)

@app.on_event("startup") 
async def startup_event():
    start_consumer() 



@app.get("/")
def root():
    return {"Connection":"Successful"}

 

@app.post("/send-email")
def send_email_to_producer(request: EmailRequest):
    send_email_message(request.to, request.subject, request.body)
    return {"status": "queued", "to": request.to}
