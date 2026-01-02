# send_email.py

import django
from django.conf import settings
from django.core.mail import send_mail
from typing import Optional

# Manual settings configuration
settings.configure(
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_HOST='smtp.gmail.com',
    EMAIL_PORT=587,
    EMAIL_USE_TLS=True,
    EMAIL_HOST_USER='hritikchoukikar2000@gmail.com',
    EMAIL_HOST_PASSWORD='dfga wzek uajl aucl',
    DEFAULT_FROM_EMAIL='hritikchoukikar2000@gmail.com'
    #dfga wzek uajl aucl
)

django.setup()


def send_email_to_user(subject,message,recip,fail_silently:Optional[bool]=False,from_email:Optional[str]=None):
    print(subject,message,recip)
    send_mail(
    subject=subject,
    message=message,
    recipient_list=[recip],
    from_email=settings.DEFAULT_FROM_EMAIL,
    
    fail_silently=fail_silently
)
