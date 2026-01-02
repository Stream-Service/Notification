
from pydantic import BaseModel, EmailStr

from pydantic import BaseModel, EmailStr

class NotificationRequest(BaseModel):
     
    user_name: str
    to: EmailStr
    type: str
    template_type: str
 