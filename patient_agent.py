"""
Main Patient Agent for Medical Appointment Scheduling AI Agent
Handles conversation flow and patient interactions
"""
import re
from datetime import datetime, timedelta
from database import PatientDatabase
from scheduler import SmartScheduler
from communication import CommunicationManager, ReportGenerator

class PatientAgent:
    def __init__(self):
        self.db = PatientDatabase()
        self.scheduler = SmartScheduler()
        self.comm_manager = CommunicationManager()
        self.report_generator = ReportGenerator()
        self.conversation_state = {}
        self.reset_conversation()

    def reset_conversation(self):
        """Reset conversation state"""
        self.conversation_state = {
            'step': 'greeting',
            'patient_info': {},
            'appointment_info': {},
            'collected_data': {
                'name': None,
                'dob': None,
                'doctor': None,
                'location': None,
                'phone': None,
                'email': None,
                'insurance': {}
            }
        }

    def process_message(self, user_input):
        """Process user message and return appropriate response"""
        current_step = self.conversation_state['step']

        if current_step == 'greeting':
            return self.handle_greeting(user_input)
        elif current_step == 'collect_name':
            return self.handle_name_collection(user_input)
        elif current_step == 'collect_dob':
            return self.handle_dob_collection(user_input)
        elif current_step == 'collect_doctor':
            return self.handle_doctor_selection(user_input)
        elif current_step == 'collect_phone':
            return self.handle_phone_collection(user_input)
        elif current_step == 'collect_email':
            return self.handle_email_collection(user_input)
        elif current_step == 'show_availability':
            return self.handle_slot_selection(user_input)
        elif current_step == 'collect_insurance':
            return self.handle_insurance_collection(user_input)
        elif current_step == 'confirm_appointment':
            return self.handle_appointment_confirmation(user_input)
        else:
            return "I'm sorry, I didn't understand. Could you please try again?"

    def handle_greeting(self, user_input):
        """Handle initial greeting and start data collection"""
        self.conversation_state['step'] = 'collect_name'
        return """Welcome to Medical Center Appointment Scheduling!

I'm here to help you schedule your appointment. Let me gather some basic information.

Please provide your full name:"""

    def handle_name_collection(self, user_input):
        """Collect and validate patient name"""
        name = user_input.strip()
        if len(name) < 2:
            return "Please provide a valid full name:"

        self.conversation_state['collected_data']['name'] = name

        # Check if patient exists in database
        existing_patient = self.db.find_patient(name=name)
        if existing_patient:
            self.conversation_state['patient_info'] = existing_patient
            self.conversation_state['step'] = 'collect_doctor'
            return f"""Great! I found your information in our system.

Name: {existing_patient['name']}
Phone: {existing_patient['phone']}
Email: {existing_patient['email']}

Which doctor would you like to see? Our available doctors are:
{self.format_doctors_list()}"""
        else:
            self.conversation_state['step'] = 'collect_dob'
            return f"Thank you, {name}. I don't see you in our system, so I'll set you up as a new patient.\n\nPlease provide your date of birth (YYYY-MM-DD format):"

    def handle_dob_collection(self, user_input):
        """Collect and validate date of birth"""
        dob = user_input.strip()

        # Validate DOB format
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            if dob_date > datetime.now():
                return "Date of birth cannot be in the future. Please enter a valid date (YYYY-MM-DD):"
        except ValueError:
            return "Please enter date of birth in YYYY-MM-DD format (e.g., 1990-05-15):"

        self.conversation_state['collected_data']['dob'] = dob
        self.conversation_state['step'] = 'collect_doctor'

        return f"""Thank you. Now, which doctor would you like to see?

Our available doctors are:
{self.format_doctors_list()}

Please type the doctor's name:"""

    def handle_doctor_selection(self, user_input):
        """Handle doctor selection"""
        doctor_input = user_input.strip()

        # Find matching doctor
        all_doctors = self.db.get_all_doctors()
        selected_doctor = None

        for doctor in all_doctors:
            if doctor_input.lower() in doctor.lower() or doctor.lower() in doctor_input.lower():
                selected_doctor = doctor
                break

        if not selected_doctor:
            return f"""I didn't recognize that doctor. Please select from our available doctors:
{self.format_doctors_list()}"""

        self.conversation_state['collected_data']['doctor'] = selected_doctor
        doctor_info = self.db.get_doctor_info(selected_doctor)
        self.conversation_state['collected_data']['location'] = doctor_info['location']

        # If existing patient, go to availability
        if self.conversation_state['patient_info']:
            return self.show_availability()
        else:
            # New patient - collect contact info
            self.conversation_state['step'] = 'collect_phone'
            return "Please provide your phone number:"

    def handle_phone_collection(self, user_input):
        """Collect phone number"""
        phone = user_input.strip()

        # Basic phone validation
        if len(phone) < 10:
            return "Please provide a valid phone number:"

        self.conversation_state['collected_data']['phone'] = phone
        self.conversation_state['step'] = 'collect_email'
        return "Please provide your email address:"

    def handle_email_collection(self, user_input):
        """Collect email address"""
        email = user_input.strip()

        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return "Please provide a valid email address:"

        self.conversation_state['collected_data']['email'] = email

        # Create new patient record
        new_patient_data = {
            'name': self.conversation_state['collected_data']['name'],
            'dob': self.conversation_state['collected_data']['dob'],
            'phone': phone,
            'email': email,
            'insurance_carrier': 'TBD',
            'member_id': 'TBD',
            'group_id': 'TBD',
            'preferred_doctor': self.conversation_state['collected_data']['doctor']
        }

        self.conversation_state['patient_info'] = self.db.add_new_patient(new_patient_data)
        return self.show_availability()

    def show_availability(self):
        """Show available appointment slots"""
        doctor_name = self.conversation_state['collected_data']['doctor']
        available_slots = self.scheduler.get_available_appointments(doctor_name, num_days=14)

        if not available_slots:
            return f"I'm sorry, {doctor_name} has no available appointments in the next 2 weeks. Would you like to try a different doctor?"

        self.conversation_state['step'] = 'show_availability'
        formatted_slots = self.scheduler.format_available_slots(available_slots, limit=10)

        return f"""Here are the available appointment slots for {doctor_name}:

{formatted_slots}

Please type the number of your preferred slot:"""

    def handle_slot_selection(self, user_input):
        """Handle appointment slot selection"""
        try:
            slot_number = int(user_input.strip()) - 1
            doctor_name = self.conversation_state['collected_data']['doctor']
            available_slots = self.scheduler.get_available_appointments(doctor_name, num_days=14)

            if 0 <= slot_number < len(available_slots):
                selected_slot = available_slots[slot_number]
                self.conversation_state['appointment_info'] = selected_slot

                # Check if we have insurance info
                if not self.conversation_state['patient_info'].get('insurance_carrier') or self.conversation_state['patient_info']['insurance_carrier'] == 'TBD':
                    self.conversation_state['step'] = 'collect_insurance'
                    return """Before we confirm your appointment, I need to collect your insurance information.

Please provide:
1. Insurance carrier (e.g., Blue Cross, Aetna, Cigna)
2. Member ID
3. Group ID

You can provide all at once or one at a time. Start with your insurance carrier:"""
                else:
                    return self.show_appointment_summary()
            else:
                return "Please select a valid slot number from the list above:"
        except ValueError:
            return "Please enter the number corresponding to your preferred time slot:"

    def handle_insurance_collection(self, user_input):
        """Collect insurance information"""
        insurance_data = self.conversation_state.get('insurance_temp', {})

        if 'carrier' not in insurance_data:
            insurance_data['carrier'] = user_input.strip()
            self.conversation_state['insurance_temp'] = insurance_data
            return "Thank you. Now please provide your Member ID:"
        elif 'member_id' not in insurance_data:
            insurance_data['member_id'] = user_input.strip()
            self.conversation_state['insurance_temp'] = insurance_data
            return "Great! Finally, please provide your Group ID:"
        else:
            insurance_data['group_id'] = user_input.strip()
            self.conversation_state['collected_data']['insurance'] = insurance_data
            return self.show_appointment_summary()

    def show_appointment_summary(self):
        """Show appointment summary for confirmation"""
        patient_info = self.conversation_state['patient_info']
        appointment_slot = self.conversation_state['appointment_info']

        # Determine if returning patient for duration display
        is_returning = self.db.is_returning_patient(patient_info)
        duration = 30 if is_returning else 60

        date_obj = datetime.strptime(appointment_slot['date'], '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %B %d, %Y')
        time_12hr = datetime.strptime(appointment_slot['time'], '%H:%M').strftime('%I:%M %p')

        self.conversation_state['step'] = 'confirm_appointment'

        return f"""Please review your appointment details:

📅 **Appointment Summary**
Patient: {patient_info['name']}
Doctor: {appointment_slot['doctor_name']}
Date: {formatted_date}
Time: {time_12hr}
Location: {appointment_slot['location']}
Duration: {duration} minutes ({'Returning patient' if is_returning else 'New patient'})

Insurance: {self.conversation_state.get('insurance_temp', {}).get('carrier', patient_info.get('insurance_carrier', 'On file'))}

Type 'CONFIRM' to book this appointment or 'CANCEL' to start over:"""

    def handle_appointment_confirmation(self, user_input):
        """Handle final appointment confirmation"""
        response = user_input.strip().upper()

        if response == 'CONFIRM':
            return self.book_appointment()
        elif response == 'CANCEL':
            self.reset_conversation()
            return "Appointment booking cancelled. Type anything to start over."
        else:
            return "Please type 'CONFIRM' to book the appointment or 'CANCEL' to start over:"

    def book_appointment(self):
        """Book the appointment and send confirmations"""
        try:
            patient_info = self.conversation_state['patient_info']
            appointment_slot = self.conversation_state['appointment_info']

            # Book the appointment
            appointment, error = self.scheduler.schedule_appointment(
                patient_info,
                appointment_slot['doctor_name'],
                appointment_slot['date'],
                appointment_slot['time']
            )

            if error:
                return f"Sorry, there was an error booking your appointment: {error}\n\nPlease try selecting a different time slot."

            # Send confirmation email
            email_sent, email_msg = self.comm_manager.send_appointment_confirmation(appointment, patient_info)

            # Send intake form
            if email_sent:
                form_sent, form_msg = self.comm_manager.send_intake_form(patient_info, appointment)

            # Export to Excel for admin
            appointments_for_export = [appointment]
            excel_created, excel_path = self.report_generator.export_appointments_to_excel(appointments_for_export)

            # Reset conversation for next patient
            self.reset_conversation()

            success_message = f"""✅ **Appointment Confirmed!**

Your appointment has been successfully booked:
- Appointment ID: {appointment['appointment_id']}
- Date & Time: {appointment['date']} at {appointment['time']}
- Doctor: {appointment['doctor_name']}

📧 **Next Steps:**
- Confirmation email sent to {patient_info['email']}
- Patient intake form sent separately
- Please arrive 15 minutes early
- Bring ID and insurance card

You will receive appointment reminders via email and SMS.

Thank you for choosing our medical center!

---
Type anything to schedule another appointment."""

            return success_message

        except Exception as e:
            return f"An error occurred while booking your appointment: {str(e)}\n\nPlease try again or contact our office directly."

    def format_doctors_list(self):
        """Format the list of available doctors"""
        doctors_info = []
        for _, doctor in self.db.doctors_df.iterrows():
            doctors_info.append(f"• {doctor['doctor_name']} - {doctor['specialization']} ({doctor['location']})")
        return "\n".join(doctors_info)

    def get_conversation_history(self):
        """Get current conversation state for debugging"""
        return self.conversation_state
