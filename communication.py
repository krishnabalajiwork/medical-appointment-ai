"""
Communication module for Medical Appointment Scheduling AI Agent
Handles email and SMS notifications
"""
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from config import EMAIL_CONFIG, SMS_CONFIG
import os

class CommunicationManager:
    def __init__(self):
        self.email_config = EMAIL_CONFIG
        self.sms_config = SMS_CONFIG

    def send_email(self, to_email, subject, body, attachment_path=None):
        """Send email notification"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email']
            msg['To'] = to_email
            msg['Subject'] = subject

            # Add body to email
            msg.attach(MIMEText(body, 'html'))

            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)

            # Connect to server and send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['email'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['email'], to_email, text)
            server.quit()

            return True, "Email sent successfully"
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"

    def send_sms(self, to_phone, message):
        """Send SMS notification (simulated - would use Twilio in production)"""
        try:
            # In production, you would use Twilio or another SMS service
            # For demonstration, we'll simulate SMS sending
            print(f"SMS to {to_phone}: {message}")
            return True, "SMS sent successfully (simulated)"
        except Exception as e:
            return False, f"Failed to send SMS: {str(e)}"

    def send_appointment_confirmation(self, appointment, patient_info):
        """Send appointment confirmation email"""
        subject = "Appointment Confirmation - Medical Center"

        # Format appointment details
        date_obj = datetime.strptime(appointment['date'], '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %B %d, %Y')
        time_12hr = datetime.strptime(appointment['time'], '%H:%M').strftime('%I:%M %p')

        body = f"""
        <html>
        <head></head>
        <body>
            <h2>Appointment Confirmation</h2>
            <p>Dear {patient_info.get('name', 'Patient')},</p>

            <p>Your appointment has been successfully scheduled:</p>

            <div style="background-color: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <strong>Appointment Details:</strong><br>
                <strong>Date:</strong> {formatted_date}<br>
                <strong>Time:</strong> {time_12hr}<br>
                <strong>Doctor:</strong> {appointment['doctor_name']}<br>
                <strong>Location:</strong> {appointment['location']}<br>
                <strong>Duration:</strong> {appointment['duration']} minutes<br>
                <strong>Appointment ID:</strong> {appointment['appointment_id']}
            </div>

            <p><strong>Important Notes:</strong></p>
            <ul>
                <li>Please arrive 15 minutes before your appointment time</li>
                <li>Bring a valid ID and your insurance card</li>
                <li>You will receive a patient intake form separately</li>
            </ul>

            <p>If you need to reschedule or cancel, please contact us at least 24 hours in advance.</p>

            <p>Thank you for choosing our medical center!</p>

            <p>Best regards,<br>Medical Center Scheduling Team</p>
        </body>
        </html>
        """

        return self.send_email(patient_info.get('email'), subject, body)

    def send_intake_form(self, patient_info, appointment):
        """Send patient intake form"""
        subject = "Patient Intake Form - Please Complete Before Your Visit"

        body = f"""
        <html>
        <head></head>
        <body>
            <h2>Patient Intake Form</h2>
            <p>Dear {patient_info.get('name', 'Patient')},</p>

            <p>Please find attached the patient intake form for your upcoming appointment:</p>

            <div style="background-color: #e8f4fd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <strong>Appointment:</strong> {appointment['date']} at {appointment['time']}<br>
                <strong>Doctor:</strong> {appointment['doctor_name']}
            </div>

            <p><strong>Please complete this form and bring it with you to your appointment.</strong></p>

            <p>You can also complete it online at: <a href="#">Patient Portal Link</a></p>

            <p>Thank you!</p>

            <p>Best regards,<br>Medical Center Team</p>
        </body>
        </html>
        """

        # In production, attach actual PDF form
        return self.send_email(patient_info.get('email'), subject, body)

    def send_reminder(self, appointment, patient_info, reminder_type=1):
        """Send appointment reminders"""
        date_obj = datetime.strptime(appointment['date'], '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %B %d, %Y')
        time_12hr = datetime.strptime(appointment['time'], '%H:%M').strftime('%I:%M %p')

        if reminder_type == 1:
            # First reminder - basic
            subject = "Appointment Reminder - Tomorrow"
            body = f"""
            <html>
            <body>
                <h2>Appointment Reminder</h2>
                <p>Dear {patient_info.get('name')},</p>
                <p>This is a reminder about your appointment:</p>
                <p><strong>{formatted_date} at {time_12hr}</strong><br>
                with {appointment['doctor_name']}</p>
                <p>See you tomorrow!</p>
            </body>
            </html>
            """
        elif reminder_type == 2:
            # Second reminder - check forms
            subject = "Appointment Reminder - Have you completed your forms?"
            body = f"""
            <html>
            <body>
                <h2>Appointment Reminder</h2>
                <p>Dear {patient_info.get('name')},</p>
                <p>Your appointment is coming up: <strong>{formatted_date} at {time_12hr}</strong></p>
                <p><strong>Have you completed your patient intake forms?</strong></p>
                <p>If not, please complete them before your visit.</p>
                <p>Reply to confirm your attendance.</p>
            </body>
            </html>
            """
        else:
            # Third reminder - final confirmation
            subject = "Final Appointment Reminder - Please Confirm"
            body = f"""
            <html>
            <body>
                <h2>Final Appointment Reminder</h2>
                <p>Dear {patient_info.get('name')},</p>
                <p>Your appointment is today: <strong>{formatted_date} at {time_12hr}</strong></p>
                <p><strong>Please confirm your attendance or let us know if you need to cancel.</strong></p>
                <p>If cancelling, please provide the reason.</p>
            </body>
            </html>
            """

        # Send both email and SMS
        email_result = self.send_email(patient_info.get('email'), subject, body)
        sms_result = self.send_sms(patient_info.get('phone'), 
                                  f"Appointment reminder: {formatted_date} at {time_12hr} with {appointment['doctor_name']}")

        return email_result, sms_result

class ReportGenerator:
    def __init__(self):
        pass

    def export_appointments_to_excel(self, appointments, filename=None):
        """Export appointments to Excel for admin review"""
        if not filename:
            filename = f"appointments_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        # Create DataFrame from appointments
        df = pd.DataFrame(appointments)

        # Create outputs directory if it doesn't exist
        os.makedirs('outputs', exist_ok=True)

        filepath = os.path.join('outputs', filename)

        try:
            # Export to Excel
            df.to_excel(filepath, index=False, sheet_name='Appointments')
            return True, filepath
        except Exception as e:
            return False, str(e)

    def generate_daily_schedule(self, date, doctor_name=None):
        """Generate daily schedule report"""
        # This would query the database for appointments on a specific date
        # For now, return a placeholder
        return {
            'date': date,
            'total_appointments': 0,
            'doctors': [],
            'appointments': []
        }
