#!/usr/bin/env python
# -*- coding: utf-8 -*-

import schedule
import time
import os
import sys
import importlib
from datetime import datetime
from app.batch import batch_logger

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import batch jobs
from app.batch.mail_alert import daily_system_status_alert

def run_job(job_func, job_name):
    """Wrapper to log job execution"""
    start_time = datetime.now()
    batch_logger.info(f"Starting job: {job_name}")
    
    try:
        job_func()
        batch_logger.info(f"Job completed successfully: {job_name}")
    except Exception as e:
        batch_logger.error(f"Job failed: {job_name} - Error: {str(e)}")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    batch_logger.info(f"Job duration: {job_name} - {duration:.2f} seconds")

def setup_schedule():
    """Setup the job schedule"""
    # Daily status email at 8:00 AM
    schedule.every().day.at("08:00").do(run_job, daily_system_status_alert, "daily_system_status_alert")
    
    # Add more scheduled jobs here
    # Example: schedule.every(1).hours.do(run_job, hourly_job, "hourly_job")
    
    batch_logger.info("Scheduler initialized with jobs")

def run_scheduler():
    """Run the scheduler loop"""
    setup_schedule()
    
    batch_logger.info("Starting scheduler")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    batch_logger.info("Batch scheduler starting")
    run_scheduler() 