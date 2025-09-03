"""
Configuration file for Medical Appointment Scheduling AI Agent
"""
import os

# LLM Configuration (using OpenAI as example, can be replaced with any LLM)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

# Email Configuration (using Gmail SMTP as example)
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": os.getenv("EMAIL_ADDRESS", "your-email@gmail.com"),
    "password": os.getenv("EMAIL_PASSWORD", "your-app-password")
}

# SMS Configuration (using Twilio as example)
SMS_CONFIG = {
    "account_sid": os.getenv("TWILIO_SID", "your-twilio-sid"),
    "auth_token": os.getenv("TWILIO_TOKEN", "your-twilio-token"),
    "from_number": os.getenv("TWILIO_PHONE", "+1234567890")
}

# Database files
DATA_FILES = {
    "patients": "patients.csv",
    "doctors": "doctors.csv",
    "schedules": "schedules.csv"
}

# Appointment durations (in minutes)
APPOINTMENT_DURATIONS = {
    "new_patient": 60,
    "returning_patient": 30
}

# Form templates
INTAKE_FORM_PATH = "forms/patient_intake_form.pdf"

# Output directories
OUTPUT_DIR = "outputs"
EXCEL_REPORTS_DIR = "outputs/reports"
