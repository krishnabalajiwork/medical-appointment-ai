"""
Streamlit app for Medical Appointment Scheduling AI Agent
Main interface for the RagaAI Data Science Intern project
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Import our custom modules
from patient_agent import PatientAgent
from database import PatientDatabase
from communication import ReportGenerator
from utils import create_output_directory

# Page configuration
st.set_page_config(
    page_title="Medical Center - AI Appointment Scheduler",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = PatientAgent()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'db' not in st.session_state:
    st.session_state.db = PatientDatabase()

def main():
    # Sidebar for admin functions
    st.sidebar.title("🏥 Medical Center")
    st.sidebar.markdown("---")

    # Admin section
    st.sidebar.subheader("Admin Functions")

    if st.sidebar.button("📊 View All Patients"):
        show_admin_patients()

    if st.sidebar.button("📅 View Schedules"):
        show_admin_schedules()

    if st.sidebar.button("📁 Generate Reports"):
        generate_admin_reports()

    if st.sidebar.button("🔄 Reset Conversation"):
        st.session_state.agent.reset_conversation()
        st.session_state.messages = []
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### System Stats")

    # Show basic stats
    total_patients = len(st.session_state.db.patients_df)
    total_doctors = len(st.session_state.db.doctors_df)
    available_slots = len(st.session_state.db.schedules_df[st.session_state.db.schedules_df['available'] == True])

    st.sidebar.metric("Total Patients", total_patients)
    st.sidebar.metric("Available Doctors", total_doctors)
    st.sidebar.metric("Available Slots", available_slots)

    # Main chat interface
    st.title("🤖 AI Medical Appointment Scheduler")
    st.markdown("Welcome to our AI-powered appointment scheduling system. I'll help you book your medical appointment quickly and easily!")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = st.session_state.agent.process_message(prompt)
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Auto-start conversation if no messages
    if not st.session_state.messages:
        welcome_message = st.session_state.agent.process_message("start")
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})
        st.rerun()

def show_admin_patients():
    """Show admin view of all patients"""
    st.subheader("👥 Patient Database")

    patients_df = st.session_state.db.patients_df

    # Add search functionality
    search_term = st.text_input("🔍 Search patients by name:")
    if search_term:
        patients_df = patients_df[patients_df['name'].str.contains(search_term, case=False, na=False)]

    # Display patients table
    st.dataframe(
        patients_df,
        use_container_width=True,
        column_config={
            "patient_id": "Patient ID",
            "name": "Full Name",
            "dob": "Date of Birth",
            "phone": "Phone",
            "email": "Email",
            "insurance_carrier": "Insurance",
            "previous_visits": st.column_config.NumberColumn("Visits", format="%d")
        }
    )

    st.info(f"Total patients in database: {len(patients_df)}")

def show_admin_schedules():
    """Show admin view of schedules"""
    st.subheader("📅 Doctor Schedules & Availability")

    # Doctor selection
    doctor_names = st.session_state.db.get_all_doctors()
    selected_doctor = st.selectbox("Select Doctor:", ["All Doctors"] + doctor_names)

    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From Date:", value=datetime.now().date())
    with col2:
        end_date = st.date_input("To Date:", value=datetime.now().date())

    # Filter schedules
    schedules_df = st.session_state.db.schedules_df.copy()

    # Convert date strings to datetime for filtering
    schedules_df['date'] = pd.to_datetime(schedules_df['date']).dt.date

    # Apply filters
    if selected_doctor != "All Doctors":
        schedules_df = schedules_df[schedules_df['doctor_name'] == selected_doctor]

    schedules_df = schedules_df[
        (schedules_df['date'] >= start_date) & 
        (schedules_df['date'] <= end_date)
    ]

    # Show availability summary
    col1, col2, col3 = st.columns(3)
    with col1:
        total_slots = len(schedules_df)
        st.metric("Total Slots", total_slots)
    with col2:
        available_slots = len(schedules_df[schedules_df['available'] == True])
        st.metric("Available", available_slots)
    with col3:
        booked_slots = total_slots - available_slots
        st.metric("Booked", booked_slots)

    # Display schedules
    if len(schedules_df) > 0:
        st.dataframe(
            schedules_df,
            use_container_width=True,
            column_config={
                "date": st.column_config.DateColumn("Date"),
                "time": "Time",
                "doctor_name": "Doctor",
                "location": "Location",
                "available": st.column_config.CheckboxColumn("Available")
            }
        )
    else:
        st.info("No schedules found for the selected criteria.")

def generate_admin_reports():
    """Generate administrative reports"""
    st.subheader("📊 Administrative Reports")

    # Create output directory
    create_output_directory("outputs")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Patient Report")
        if st.button("📥 Export Patients to Excel"):
            try:
                patients_df = st.session_state.db.patients_df
                filename = f"patients_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filepath = os.path.join('outputs', filename)
                patients_df.to_excel(filepath, index=False)
                st.success(f"Patients exported to: {filename}")

                # Provide download link
                with open(filepath, "rb") as file:
                    st.download_button(
                        label="📁 Download Patients Report",
                        data=file.read(),
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Error generating report: {e}")

    with col2:
        st.write("### Schedule Report")
        if st.button("📥 Export Schedules to Excel"):
            try:
                schedules_df = st.session_state.db.schedules_df
                filename = f"schedules_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filepath = os.path.join('outputs', filename)
                schedules_df.to_excel(filepath, index=False)
                st.success(f"Schedules exported to: {filename}")

                # Provide download link
                with open(filepath, "rb") as file:
                    st.download_button(
                        label="📁 Download Schedules Report",
                        data=file.read(),
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Error generating report: {e}")

    # Summary statistics
    st.write("### System Summary")

    patients_df = st.session_state.db.patients_df
    schedules_df = st.session_state.db.schedules_df

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Patients", len(patients_df))
    with col2:
        returning_patients = len(patients_df[patients_df['previous_visits'] > 0])
        st.metric("Returning Patients", returning_patients)
    with col3:
        available_slots = len(schedules_df[schedules_df['available'] == True])
        st.metric("Available Slots", available_slots)
    with col4:
        total_slots = len(schedules_df)
        booked_percentage = ((total_slots - available_slots) / total_slots * 100) if total_slots > 0 else 0
        st.metric("Booking Rate", f"{booked_percentage:.1f}%")

if __name__ == "__main__":
    main()
