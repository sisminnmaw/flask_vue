#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime
from app.batch import batch_logger

def send_alert_email(recipients, subject, body):
    """Send email alert to the specified recipients"""
    try:
        # Get email configuration from environment variables or use defaults
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.example.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SMTP_USERNAME', 'alert@example.com')
        smtp_password = os.environ.get('SMTP_PASSWORD', 'password')
        sender_email = os.environ.get('SENDER_EMAIL', 'alert@example.com')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to server and send
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        batch_logger.info(f"Email alert sent to {recipients}")
        return True
    except Exception as e:
        batch_logger.error(f"Failed to send email alert: {str(e)}")
        return False

def daily_system_status_alert():
    """Daily system status check and alert"""
    batch_logger.info("Running daily system status check")
    
    # This would typically check system metrics, database status, etc.
    # Here we're just simulating with a basic message
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    recipients = ['admin@example.com']
    subject = f"Daily System Status Report - {current_time}"
    body = f"""
    System Status Report
    Time: {current_time}
    
    All systems operational.
    Database connections: OK
    API Services: OK
    Batch Processing: OK
    
    This is an automated message.
    """
    
    return send_alert_email(recipients, subject, body)

if __name__ == "__main__":
    batch_logger.info("Starting mail alert batch job")
    daily_system_status_alert()
    batch_logger.info("Completed mail alert batch job") 