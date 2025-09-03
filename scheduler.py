"""
Smart scheduling logic for Medical Appointment Scheduling AI Agent
"""
from datetime import datetime, timedelta
from database import PatientDatabase
from config import APPOINTMENT_DURATIONS

class SmartScheduler:
    def __init__(self):
        self.db = PatientDatabase()

    def determine_appointment_duration(self, patient_info):
        """Determine appointment duration based on patient type"""
        if self.db.is_returning_patient(patient_info):
            return APPOINTMENT_DURATIONS["returning_patient"]  # 30 minutes
        else:
            return APPOINTMENT_DURATIONS["new_patient"]  # 60 minutes

    def get_available_appointments(self, doctor_name, preferred_date=None, num_days=7):
        """Get available appointment slots"""
        if preferred_date:
            # Get slots for specific date
            duration = 60  # Default, will be adjusted based on patient type
            return self.db.get_available_slots(doctor_name, preferred_date, duration)
        else:
            # Get slots for next few days
            today = datetime.now().date()
            all_slots = []

            for day_offset in range(num_days):
                date = (today + timedelta(days=day_offset)).strftime('%Y-%m-%d')
                slots = self.db.get_available_slots(doctor_name, date, 60)
                all_slots.extend(slots)

            return all_slots

    def schedule_appointment(self, patient_info, doctor_name, date, time):
        """Schedule an appointment"""
        # Determine appointment duration
        duration = self.determine_appointment_duration(patient_info)

        # Verify slot is still available
        available_slots = self.db.get_available_slots(doctor_name, date, duration)
        slot_available = any(
            slot['date'] == date and slot['time'] == time 
            for slot in available_slots
        )

        if not slot_available:
            return None, "Selected time slot is no longer available"

        # Book the appointment
        try:
            appointment = self.db.book_appointment(doctor_name, date, time, duration, patient_info)
            return appointment, None
        except Exception as e:
            return None, f"Error booking appointment: {str(e)}"

    def format_available_slots(self, slots, limit=10):
        """Format available slots for display"""
        if not slots:
            return "No available slots found."

        formatted_slots = []
        for i, slot in enumerate(slots[:limit]):
            date_obj = datetime.strptime(slot['date'], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%A, %B %d, %Y')
            time_12hr = datetime.strptime(slot['time'], '%H:%M').strftime('%I:%M %p')

            formatted_slots.append(
                f"{i+1}. {formatted_date} at {time_12hr} - {slot['location']}"
            )

        return "\n".join(formatted_slots)

    def validate_appointment_request(self, doctor_name, date, time):
        """Validate appointment request"""
        errors = []

        # Check if doctor exists
        if doctor_name not in self.db.get_all_doctors():
            errors.append(f"Doctor '{doctor_name}' not found")

        # Check date format and validity
        try:
            requested_date = datetime.strptime(date, '%Y-%m-%d').date()
            if requested_date < datetime.now().date():
                errors.append("Cannot schedule appointments in the past")
        except ValueError:
            errors.append("Invalid date format. Please use YYYY-MM-DD")

        # Check time format
        try:
            datetime.strptime(time, '%H:%M')
        except ValueError:
            errors.append("Invalid time format. Please use HH:MM (24-hour format)")

        return errors
