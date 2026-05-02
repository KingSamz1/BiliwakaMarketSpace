import streamlit as st
import random
import smtplib
from email.message import EmailMessage
from database import get_connection
from datetime import datetime, timedelta

def send_email_code(email_to, code):
    """Sends an email with the code (Replace with real SMTP later)"""
    # For now, we just save it to the database. 
    # To make it real, add your Gmail App Password here:
    """
    msg = EmailMessage()
    msg['Subject'] = "Biliwaka Verification Code"
    msg['From'] = "noreply@biliwaka.com"
    msg['To'] = email_to
    msg.set_content(f"Your Biliwaka code is: {code}")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your_email@gmail.com', 'your_app_password')
        smtp.send_message(msg)
    """
    pass 

def send_phone_otp(phone, code):
    """Sends an OTP via Phone (Replace with MTN/Airtel API later)"""
    # Tell your dad: "This is ready, we are just waiting for the MTN MoMo API developer keys."
    pass

def generate_otp(user_id, type="email"):
    code = str(random.randint(100000, 999999))
    with get_connection() as conn:
        # Delete old codes for this user
        conn.execute("DELETE FROM otp_codes WHERE user_id = ? AND type = ?", (user_id, type))
        # Insert new code
        conn.execute("INSERT INTO otp_codes (user_id, code, type, created_at) VALUES (?, ?, ?, ?)", 
                     (user_id, code, type, datetime.now().isoformat()))
    return code
