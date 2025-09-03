"""
Database operations for Medical Appointment Scheduling AI Agent
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import DATA_FILES
import os

class PatientDatabase:
    def __init__(self):
        self.patients_df = pd.read_csv(DATA_FILES["patients"])
        self.doctors_df = pd.read_csv(DATA_FILES["doctors"])
        self.schedules_df = pd.read_csv(DATA_FILES["schedules"])

    def find_patient(self, name=None, dob=None, phone=None):
        """Find patient by name, DOB, or phone"""
        query_conditions = []

        if name:
            query_conditions.append(self.patients_df['name'].str.contains(name, case=False, na=False))
        if dob:
            query_conditions.append(self.patients_df['dob'] == dob)
        if phone:
            query_conditions.append(self.patients_df['phone'] == phone)

        if not query_conditions:
            return None

        # Combine conditions with AND logic
        combined_condition = query_conditions[0]
        for condition in query_conditions[1:]:
            combined_condition = combined_condition & condition

        results = self.patients_df[combined_condition]
        return results.iloc[0].to_dict() if len(results) > 0 else None

    def is_returning_patient(self, patient_info):
        """Check if patient is returning (has previous visits)"""
        if patient_info and 'previous_visits' in patient_info:
            return patient_info['previous_visits'] > 0
        return False

    def get_doctor_info(self, doctor_name):
        """Get doctor information"""
        doctor = self.doctors_df[self.doctors_df['doctor_name'] == doctor_name]
        return doctor.iloc[0].to_dict() if len(doctor) > 0 else None

    def get_available_slots(self, doctor_name, date=None, duration=60):
        """Get available appointment slots for a doctor"""
        query = (self.schedules_df['doctor_name'] == doctor_name) & (self.schedules_df['available'] == True)

        if date:
            query = query & (self.schedules_df['date'] == date)

        available_slots = self.schedules_df[query].copy()

        # Filter slots that have enough consecutive time for the appointment duration
        filtered_slots = []
        for _, slot in available_slots.iterrows():
            slot_datetime = pd.to_datetime(f"{slot['date']} {slot['time']}")
            end_time = slot_datetime + timedelta(minutes=duration)

            # Check if there are enough consecutive slots
            if duration <= 30:  # Single slot needed
                filtered_slots.append(slot.to_dict())
            else:  # Multiple slots needed
                next_slot_time = slot_datetime + timedelta(minutes=30)
                next_slot_query = (
                    (self.schedules_df['doctor_name'] == doctor_name) &
                    (self.schedules_df['date'] == slot['date']) &
                    (self.schedules_df['time'] == next_slot_time.strftime('%H:%M')) &
                    (self.schedules_df['available'] == True)
                )
                if len(self.schedules_df[next_slot_query]) > 0:
                    filtered_slots.append(slot.to_dict())

        return filtered_slots

    def book_appointment(self, doctor_name, date, time, duration, patient_info):
        """Book an appointment slot"""
        # Mark the primary slot as unavailable
        primary_slot_query = (
            (self.schedules_df['doctor_name'] == doctor_name) &
            (self.schedules_df['date'] == date) &
            (self.schedules_df['time'] == time)
        )
        self.schedules_df.loc[primary_slot_query, 'available'] = False

        # If duration > 30 minutes, mark next slot as unavailable too
        if duration > 30:
            next_time = (datetime.strptime(time, '%H:%M') + timedelta(minutes=30)).strftime('%H:%M')
            next_slot_query = (
                (self.schedules_df['doctor_name'] == doctor_name) &
                (self.schedules_df['date'] == date) &
                (self.schedules_df['time'] == next_time)
            )
            self.schedules_df.loc[next_slot_query, 'available'] = False

        # Save updated schedules
        self.schedules_df.to_csv(DATA_FILES["schedules"], index=False)

        # Create appointment record
        appointment = {
            'appointment_id': f'APT{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'patient_id': patient_info.get('patient_id', 'NEW'),
            'patient_name': patient_info.get('name'),
            'doctor_name': doctor_name,
            'date': date,
            'time': time,
            'duration': duration,
            'location': self.get_doctor_info(doctor_name)['location'],
            'status': 'confirmed',
            'created_at': datetime.now().isoformat()
        }

        return appointment

    def get_all_doctors(self):
        """Get list of all doctors"""
        return self.doctors_df['doctor_name'].tolist()

    def add_new_patient(self, patient_data):
        """Add new patient to database"""
        new_patient_id = f"P{len(self.patients_df) + 1:03d}"
        patient_data['patient_id'] = new_patient_id
        patient_data['previous_visits'] = 0

        # Add to dataframe
        new_patient_df = pd.DataFrame([patient_data])
        self.patients_df = pd.concat([self.patients_df, new_patient_df], ignore_index=True)

        # Save to file
        self.patients_df.to_csv(DATA_FILES["patients"], index=False)

        return patient_data
