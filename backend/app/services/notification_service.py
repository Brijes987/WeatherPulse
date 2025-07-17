import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import httpx
from app.core.config import settings

class NotificationService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.twilio_sid = settings.TWILIO_ACCOUNT_SID
        self.twilio_token = settings.TWILIO_AUTH_TOKEN
        self.twilio_phone = settings.TWILIO_PHONE_NUMBER
    
    async def send_email_alert(self, to_email: str, subject: str, message: str):
        """Send email alert using SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Create HTML email body
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                        <h1 style="color: white; margin: 0;">🌤️ Weather Alert</h1>
                    </div>
                    <div style="padding: 20px; background: #f8f9fa;">
                        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <h2 style="color: #333; margin-top: 0;">Alert Notification</h2>
                            <p style="color: #666; font-size: 16px; line-height: 1.5;">{message}</p>
                            <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 5px;">
                                <strong>⚠️ Action Required:</strong> Please check your weather dashboard for more details.
                            </div>
                        </div>
                    </div>
                    <div style="text-align: center; padding: 20px; color: #666; font-size: 12px;">
                        <p>Weather Monitoring System | Powered by OpenWeatherMap</p>
                    </div>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.smtp_username, to_email, text)
            server.quit()
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    async def send_sms_alert(self, to_phone: str, message: str):
        """Send SMS alert using Twilio"""
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json"
            
            data = {
                'From': self.twilio_phone,
                'To': to_phone,
                'Body': f"🌤️ Weather Alert: {message}"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    data=data,
                    auth=(self.twilio_sid, self.twilio_token)
                )
                
                if response.status_code == 201:
                    print(f"SMS sent successfully to {to_phone}")
                    return True
                else:
                    print(f"Failed to send SMS to {to_phone}: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"Failed to send SMS to {to_phone}: {str(e)}")
            return False
    
    async def send_bulk_notifications(self, notifications: List[dict]):
        """Send multiple notifications concurrently"""
        tasks = []
        
        for notification in notifications:
            if notification['type'] == 'email':
                task = self.send_email_alert(
                    notification['recipient'],
                    notification['subject'],
                    notification['message']
                )
            elif notification['type'] == 'sms':
                task = self.send_sms_alert(
                    notification['recipient'],
                    notification['message']
                )
            
            tasks.append(task)
        
        # Execute all notifications concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results