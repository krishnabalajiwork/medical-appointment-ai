"""
Utility functions for Medical Appointment Scheduling AI Agent
"""
from datetime import datetime, timedelta
import re
import pandas as pd
import os

def validate_date_format(date_string, format_string='%Y-%m-%d'):
    """Validate date format"""
    try:
        datetime.strptime(date_string, format_string)
        return True
    except ValueError:
        return False

def validate_time_format(time_string, format_string='%H:%M'):
    """Validate time format"""
    try:
        datetime.strptime(time_string, format_string)
        return True
    except ValueError:
        return False

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number"""
    # Remove non-digit characters
    phone_digits = re.sub(r'\D', '', phone)
    # Check if it has 10 or 11 digits
    return len(phone_digits) >= 10

def format_phone(phone):
    """Format phone number"""
    phone_digits = re.sub(r'\D', '', phone)
    if len(phone_digits) == 10:
        return f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}"
    elif len(phone_digits) == 11:
        return f"+{phone_digits[0]} ({phone_digits[1:4]}) {phone_digits[4:7]}-{phone_digits[7:]}"
    return phone

def get_next_weekday(target_day, start_date=None):
    """Get the next occurrence of a specific weekday"""
    if not start_date:
        start_date = datetime.now().date()

    days_ahead = target_day - start_date.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7

    return start_date + timedelta(days_ahead)

def create_output_directory(directory_name):
    """Create output directory if it doesn't exist"""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        return f"Created directory: {directory_name}"
    return f"Directory already exists: {directory_name}"

def log_appointment_activity(activity_type, details, log_file='appointment_log.txt'):
    """Log appointment activities"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {activity_type}: {details}\n"

    try:
        with open(log_file, 'a') as f:
            f.write(log_entry)
        return True
    except Exception as e:
        print(f"Logging error: {e}")
        return False

def parse_natural_date(date_input):
    """Parse natural language date input"""
    today = datetime.now().date()
    date_input = date_input.lower().strip()

    # Handle common phrases
    if 'today' in date_input:
        return today.strftime('%Y-%m-%d')
    elif 'tomorrow' in date_input:
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')
    elif 'next week' in date_input:
        return (today + timedelta(days=7)).strftime('%Y-%m-%d')

    # Handle weekday names
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for i, day in enumerate(weekdays):
        if day in date_input:
            next_occurrence = get_next_weekday(i, today)
            return next_occurrence.strftime('%Y-%m-%d')

    # Try to parse as regular date
    try:
        if '/' in date_input:
            parsed_date = datetime.strptime(date_input, '%m/%d/%Y').date()
        elif '-' in date_input:
            parsed_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        else:
            return None

        return parsed_date.strftime('%Y-%m-%d')
    except ValueError:
        return None

def format_duration(minutes):
    """Format duration in minutes to human readable format"""
    if minutes < 60:
        return f"{minutes} minutes"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours > 1 else ''} and {remaining_minutes} minutes"

def get_business_days(start_date, num_days):
    """Get business days (Monday-Friday) from start date"""
    business_days = []
    current_date = start_date

    while len(business_days) < num_days:
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            business_days.append(current_date)
        current_date += timedelta(days=1)

    return business_days

class InputValidator:
    """Class for validating various types of user input"""

    @staticmethod
    def validate_name(name):
        """Validate patient name"""
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long"

        if not re.match(r"^[a-zA-Z\s'-]+$", name.strip()):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes"

        return True, "Valid name"

    @staticmethod
    def validate_dob(dob_string):
        """Validate date of birth"""
        try:
            dob = datetime.strptime(dob_string, '%Y-%m-%d').date()

            # Check if date is not in the future
            if dob > datetime.now().date():
                return False, "Date of birth cannot be in the future"

            # Check if person is not too old (reasonable limit)
            age = (datetime.now().date() - dob).days // 365
            if age > 120:
                return False, "Please check the date of birth"

            return True, "Valid date of birth"

        except ValueError:
            return False, "Please use YYYY-MM-DD format (e.g., 1990-05-15)"

    @staticmethod
    def validate_insurance_member_id(member_id):
        """Validate insurance member ID"""
        if not member_id or len(member_id.strip()) < 3:
            return False, "Member ID must be at least 3 characters"

        return True, "Valid member ID"

def generate_appointment_reminder_text(appointment, patient_name, reminder_type=1):
    """Generate reminder text for different reminder types"""
    date_obj = datetime.strptime(appointment['date'], '%Y-%m-%d')
    formatted_date = date_obj.strftime('%A, %B %d')
    time_12hr = datetime.strptime(appointment['time'], '%H:%M').strftime('%I:%M %p')

    if reminder_type == 1:
        return f"Reminder: {patient_name}, you have an appointment on {formatted_date} at {time_12hr} with {appointment['doctor_name']}. Please arrive 15 minutes early."
    elif reminder_type == 2:
        return f"Hi {patient_name}, your appointment with {appointment['doctor_name']} is on {formatted_date} at {time_12hr}. Have you completed your intake forms? Please confirm your attendance."
    else:
        return f"Final reminder: {patient_name}, your appointment is TODAY at {time_12hr} with {appointment['doctor_name']}. Please confirm attendance or notify us if you need to cancel."
