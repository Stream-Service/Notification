# from core.database import get_db
# from core.config import setting
# from notifications_template.models import Templates,SMS
# from fastapi import APIRouter,Depends,HTTPException,status
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from producers.producer_admin import send_email_message
# from jinja2 import Template
# import redis 
# import random
# r = redis.Redis(host=setting.REDIS_SERVER, port=setting.REDIS_PORT, db=0)

# router=APIRouter(prefix="/database",tags=["database"])

# class TemplateEmailRequest(BaseModel): 
#     to: str 
#     template_name: str 
#     user_name: str

# @router.get("/template/{template_name}")
# def get_email_template(template_name:str,db:Session=Depends(get_db)):

#     template_data=db.query(Templates).filter(Templates.template_key==template_name).first()
#     if not template_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return {
#         "subject": template_data.subject,
#         "temp_text": template_data.temp_text
#     }

# @router.post("/send-template-email")
# def send_template_email(request: TemplateEmailRequest, db: Session = Depends(get_db)):
#     # Fetch template from database
#     template_data = db.query(Templates).filter(
#         Templates.template_key == request.template_name
#     ).first()
#     if not template_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

#     # Render subject and body with Jinja2
#     subject_template = Template(template_data.subject)
#     subject_str = subject_template.render(user_name=request.user_name)

#     body_template = Template(template_data.temp_text)
#     body_str = body_template.render(user_name=request.user_name)

#     # Send email
#     send_email_message(request.to, subject_str, body_str)

#     return {"status": "queued", "to": request.to, "template": request.template_name}

# @router.get("/sms/{template_name}")
# def get_sms_template(template_name:str,db:Session=Depends(get_db)):

#     template_data=db.query(SMS).filter(SMS.template_key==template_name).first()
#     if not template_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return {
#         "subject": template_data.subject,
#         "temp_text": template_data.temp_text
#     }
    
 
# def generate_otp():
#     return str(random.randint(100000, 999999))


# @router.post("/send-otp-email")
# def send_otp_email(email: str,db: Session = Depends(get_db)):
#     otp = generate_otp()
#     r.setex(f"otp:{email}", 600, otp)  # store OTP for 10 minutes

#     template_data = db.query(Templates).filter(Templates.template_key == "otp").first()
#     if not template_data:
#         raise HTTPException(status_code=404, detail="OTP template not found")

#     subject_template = Template(template_data.subject)
     
#     subject_template = Template(template_data.subject) 
#     subject_str = subject_template.render() 
#     body_template = Template(template_data.temp_text)
#     body_str = body_template.render(otp_code=otp)

#     send_email_message(email, subject_str, body_str)
#     return {"status": "sent", "to": email}

# @router.post("/verify-otp")
# def verify_otp(email: str, otp: str):
#     cached_otp = r.get(f"otp:{email}")
#     if not cached_otp:
#         raise HTTPException(status_code=400, detail="OTP expired or not found")

#     if cached_otp.decode("utf-8") != otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP")

#     # OTP is valid → mark user as verified for password reset
#     r.setex(f"verified:{email}", 600, "true")  # valid for 10 minutes
#     r.delete(f"otp:{email}")
#     return {"status": "verified", "message": "OTP verified, proceed to reset password"}
