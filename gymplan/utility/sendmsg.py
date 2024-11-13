import smtplib
import os
from dotenv import load_dotenv
from random import randint
from email.mime.text import MIMEText

load_dotenv(r"C:\Users\mike.mat\Desktop\GymRoutineMaker\senderpass.env")

#chatgpt used for refactor

SENDER = "gymplanotp@gmail.com"
SENDER_PASS = os.getenv('sp')


def genOTP() -> int:
    """Generate a OTP."""
    return randint(100000, 999999)

def sendOTP(address: str) -> int:
    """
    Adress: Recipent Email Adress
    """

    OTP = genOTP()
    
    # HTML email body with OTP
    body = f"""
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 20px;">
        <table role="presentation" width="100%" style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <tr>
                <td style="text-align: center; padding: 10px 0;">
                    <h2 style="font-size: 24px; color: #333333; margin: 0;">Your OTP Code</h2>
                    <p style="font-size: 16px; color: #666666; margin: 10px 0 20px;">Use the code below to complete your verification process:</p>
                    <div style="font-size: 32px; font-weight: bold; color: #0073e6; padding: 10px; border: 1px solid #0073e6; display: inline-block; border-radius: 5px;">
                        {OTP}
                    </div>
                </td>
            </tr>
        </table>
    </body>
    """

    # Prepare the email message
    msg = MIMEText(body, 'html')
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = SENDER
    msg['To'] = address

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER, SENDER_PASS)
        server.sendmail(SENDER, address, msg.as_string())

    return OTP

if __name__ == "__main__":
    print(sendOTP('michaelmatiychenko@gmail.com'))