import smtplib
from email.message import EmailMessage

def send_signup_email(user_email):
    EMAIL_ADDRESS = "hritikchoukikarwork24@gmail.com" # YOUR Gmail
    EMAIL_PASSWORD = ""# The 16-char App Password (NOT your normal password)

    msg = EmailMessage()
    msg['Subject'] = 'Welcome to My App!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_email
    msg.set_content("Thanks for signing up! We are glad to have you.")

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"Email sent successfully to {user_email}")
            
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage:
if __name__ == "__main__":
    new_user = "hritikchoukikar2000@gmail.com"
    send_signup_email(new_user)