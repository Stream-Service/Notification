from core.database import get_db
from notifications_template.models import Templates,SMS
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

router=APIRouter(prefix="/database",tags=["database"])


@router.get("/template/{template_name}")
def get_email_template(template_name:str,db:Session=Depends(get_db)):

    template_data=db.query(Templates).filter(Templates.template_key==template_name).first()
    if not template_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {
        "subject": template_data.subject,
        "temp_text": template_data.temp_text
    }
    

@router.get("/sms/{template_name}")
def get_sms_template(template_name:str,db:Session=Depends(get_db)):

    template_data=db.query(SMS).filter(SMS.template_key==template_name).first()
    if not template_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {
        "subject": template_data.subject,
        "temp_text": template_data.temp_text
    }
    

