import smtplib

from random import randint
from email.message import EmailMessage
from email.mime.text import MIMEText

def genOTP() -> int: return randint(100000,999999)

SENDER = "gymplanotp@gmail.com"

def sendOTP(address: str) -> int:
    msg = EmailMessage()
    msg['Subject'] = 'One time OTP'
    msg['From'] = SENDER
    msg['To'] = address
    pass
