from kafka import KafkaConsumer, KafkaProducer
import json
from core.config import setting

producer = KafkaProducer(
    bootstrap_servers=[setting.KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

consumer = KafkaConsumer(
    'user_events', 
    group_id='notify_router_group',
    bootstrap_servers=[setting.KAFKA_BOOTSTRAP_SERVERS],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
) 

# --- EMAIL TEMPLATES ---
TEMPLATE_MAP = {
    "USER_CREATED": {
        "EMAIL": {
            "subject": "Welcome to the App!",
            "body": """
                <h2>Welcome, {firstname}! 🎉</h2> 
                <p>We are thrilled to have you on board. Get ready to explore and connect!</p>
                <p>If you have any questions, feel free to reply to this email.</p>
                <p>Best,<br>The App Team</p>
            """
        }
    },
    "CHECK_OTP": {
        "EMAIL": {
            "subject": "Your Verification Code",
            "body": """
                <h2>Action Required: Verify your account</h2>
                <p>Your one-time password (OTP) is: <strong style="font-size: 24px;">{otp}</strong></p>
                <p>Please enter this code in the app to proceed. This code will expire in 10 minutes.</p>
                <p style="color: red;">Do not share this code with anyone.</p>
            """
        }
    },
    "FORGOT_PASSWORD": {
        "EMAIL": {
            "subject": "Password Reset Request",
            "body": """
                <h2>Password Reset</h2>
                <p>Hi {firstname},</p>
                <p>We received a request to reset your password. Your password reset OTP is:</p>
                <p><strong style="font-size: 24px;">{otp}</strong></p>
                <p>If you did not request a password reset, you can safely ignore this email and your password will remain unchanged.</p>
            """
        }
    },
    "NEW_FOLLOWER": {
        "EMAIL": {
            "subject": "You have a new follower!",
            "body": """
                <h2>Great news, {firstname}! 🌟</h2>
                <p><strong>{follower_name}</strong> just started following you.</p>
                <p>Log in to your account to see their profile and see what they're up to.</p>
            """
        }
    },
    "NEW_PASSWORD": {
        "EMAIL": {
            "subject": "Your New Password",
            "body": """
                <h2>Hello {firstname},</h2>
                <p>Your password has been successfully reset. Here is your new temporary password:</p>
                <p><strong style="font-size: 24px; color: #4CAF50;">{new_password}</strong></p>
                <p>Please log in using this password. We highly recommend changing it from your account settings once you are logged in.</p>
                <p>If you did not request this change, please contact support immediately.</p>
                <p>Best regards,<br>The App Team</p>
            """
        }
    },
}
# your kafka file — wrap everything in a function
def start():
    print("Router Service Started... Listening for events to route via Email.",flush=True)
    
    for msg in consumer:
        event = msg.value
        event_type = event.get('event_type')
        raw_data = event.get('data')
        
        print(f"\nReceived event: {event_type}")

        if not raw_data:
            print("Error: Event received without 'data' block.", flush=True)
            continue

        if event_type not in TEMPLATE_MAP:
            continue

        channel_templates = TEMPLATE_MAP[event_type]

        if "EMAIL" in channel_templates:
            email_tmpl = channel_templates.get('EMAIL')
            try:
                email_payload = {
                    "to": raw_data.get('email'),
                    "subject": email_tmpl["subject"].format(**raw_data),
                    "body": email_tmpl["body"].format(**raw_data)
                }
                print(f"Email::::", email_tmpl, flush=True)
                producer.send('notify.email', value=email_payload)
                print(f"✅ Routed {event_type} to Email for {raw_data.get('email')}", flush=True)
            except KeyError as e:
                print(f"❌ Missing required data field for {event_type} template: {e}")

        producer.flush()