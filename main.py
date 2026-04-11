from fastapi import FastAPI
# from notifications_template.routes import router as noti_router
# from database_template.template import router as db_router
# # from tracker import start_consumer
from producers.producer_admin import send_email_message
from fastapi.middleware.cors import CORSMiddleware
import router
from contextlib import asynccontextmanager
import email_sender
import asyncio 
from pydantic import BaseModel
 
import threading

# Define request body schema
class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

 
from core.database import engine,Base_model

Base_model.metadata.create_all(bind=engine)



@asynccontextmanager
async def lifespan(app: FastAPI):
     
    threading.Thread(target=router.start, daemon=True).start()
     
    threading.Thread(target=email_sender.start, daemon=True).start()
    yield


app = FastAPI(lifespan=lifespan)
 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow everything for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 

 



@app.get("/")
def root():
    return {"Connection":"Successful"}

 

@app.post("/send-email")
def send_email_to_producer(request: EmailRequest):
    send_email_message(request.to, request.subject, request.body)
    return {"status": "queued", "to": request.to}
