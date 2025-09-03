# Medical Appointment Scheduling AI Agent

**Data Science Intern - RagaAI Case Study Project**

An AI-powered medical appointment scheduling system that automates patient booking, reduces no-shows, and streamlines clinic operations.

## 🎯 Project Overview

This project implements a comprehensive medical appointment scheduling system with the following capabilities:

- **Patient Greeting & Data Collection**: Collects name, DOB, doctor preference, and contact information
- **Smart Patient Lookup**: Detects new vs returning patients from database
- **Intelligent Scheduling**: 60-minute slots for new patients, 30-minute for returning patients
- **Calendar Integration**: Shows available appointment slots with real-time booking
- **Insurance Collection**: Captures insurance details (carrier, member ID, group)
- **Appointment Confirmation**: Exports to Excel and sends email confirmations
- **Form Distribution**: Automated patient intake form delivery
- **Reminder System**: 3 automated reminders with follow-up actions

## 🏗️ Architecture

### Technical Stack
- **Backend**: Python with custom agent framework
- **Frontend**: Streamlit for interactive UI
- **Database**: CSV files simulating EMR system
- **Communication**: Email (SMTP) and SMS integration
- **Data Export**: Excel reports for administrative review

### Core Components

1. **PatientAgent** (`patient_agent.py`): Main conversational AI agent
2. **Database** (`database.py`): Patient and schedule data management
3. **SmartScheduler** (`scheduler.py`): Appointment booking logic
4. **CommunicationManager** (`communication.py`): Email/SMS notifications
5. **Streamlit App** (`main.py`): Web interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone/Download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional for full functionality):
   ```bash
   # For email notifications
   export EMAIL_ADDRESS="your-email@gmail.com"
   export EMAIL_PASSWORD="your-app-password"

   # For SMS notifications (Twilio)
   export TWILIO_SID="your-twilio-sid"
   export TWILIO_TOKEN="your-twilio-token"
   export TWILIO_PHONE="+1234567890"
   ```

4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

5. **Access the application**:
   - Open your browser to `http://localhost:8501`
   - Start scheduling appointments through the chat interface

## 📊 Sample Data

The system comes pre-configured with sample data:

- **50 synthetic patients** with various medical histories
- **4 doctors** with different specializations and schedules
- **30 days** of available appointment slots
- **Realistic scheduling constraints** and business rules

### Doctors Available:
- **Dr. Smith** - General Practice (Main Clinic)
- **Dr. Johnson** - Cardiology (Heart Center)
- **Dr. Williams** - Dermatology (Skin Clinic)
- **Dr. Brown** - Orthopedics (Bone & Joint Center)

## 🎮 Usage Guide

### Booking an Appointment

1. **Start Conversation**: The AI agent will greet you
2. **Provide Information**: Enter your name and contact details
3. **Select Doctor**: Choose from available doctors
4. **Pick Time Slot**: Select from available appointments
5. **Insurance Details**: Provide insurance information
6. **Confirm Booking**: Review and confirm your appointment

### Admin Functions

Access admin features through the sidebar:

- **View All Patients**: Browse patient database
- **View Schedules**: Check doctor availability
- **Generate Reports**: Export data to Excel
- **Reset Conversation**: Start fresh chat session

## 🔧 Configuration

### Email Setup (Gmail Example)

1. Enable 2-factor authentication on your Gmail account
2. Generate an "App Password" in Google Account settings
3. Use your email and app password in environment variables

### SMS Setup (Twilio)

1. Create a Twilio account at https://www.twilio.com
2. Get your Account SID, Auth Token, and phone number
3. Add credentials to environment variables

## 📁 File Structure

```
medical-appointment-ai/
├── main.py                 # Streamlit web application
├── patient_agent.py        # Main AI agent logic
├── database.py            # Database operations
├── scheduler.py           # Smart scheduling logic
├── communication.py       # Email/SMS handling
├── utils.py              # Utility functions
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── patients.csv          # Sample patient data
├── doctors.csv           # Doctor information
├── schedules.csv         # Available time slots
└── outputs/              # Generated reports
```

## ✨ Key Features

### Intelligent Patient Detection
- Automatically identifies returning vs new patients
- Adjusts appointment duration accordingly
- Maintains patient history and preferences

### Smart Scheduling
- **New Patients**: 60-minute appointments
- **Returning Patients**: 30-minute appointments  
- **Real-time Availability**: Updates slots immediately
- **Conflict Prevention**: Prevents double-booking

### Comprehensive Communication
- **Confirmation Emails**: Detailed appointment information
- **Intake Forms**: Automated form distribution
- **Reminder System**: 3-tier reminder workflow
- **SMS Integration**: Text message notifications

### Administrative Tools
- **Patient Management**: View and search patient database
- **Schedule Oversight**: Monitor doctor availability
- **Excel Reports**: Export data for analysis
- **Real-time Metrics**: Track system performance

## 🔍 Demo Workflow

1. **Patient Greeting**: "Welcome to Medical Center..."
2. **Data Collection**: Name, DOB, contact information
3. **Doctor Selection**: Choose from available specialists
4. **Slot Selection**: Pick from available time slots
5. **Insurance Information**: Capture insurance details
6. **Confirmation**: Review and confirm appointment
7. **Automated Follow-up**: Emails, forms, and reminders

## 📈 Business Impact

- **Reduced No-shows**: Automated reminder system
- **Improved Efficiency**: Streamlined booking process
- **Better Data Management**: Centralized patient information
- **Enhanced Patient Experience**: 24/7 scheduling availability
- **Administrative Insights**: Comprehensive reporting

## 🛠️ Customization

### Adding New Doctors
1. Edit `doctors.csv` to add new doctor information
2. Update availability schedules in `schedules.csv`
3. Restart the application

### Modifying Appointment Types
1. Update `APPOINTMENT_DURATIONS` in `config.py`
2. Adjust scheduling logic in `scheduler.py`

### Custom Communication Templates
1. Modify email templates in `communication.py`
2. Customize SMS message formats
3. Add new reminder types

## 🚨 Error Handling

The system includes comprehensive error handling for:
- Invalid date/time inputs
- Scheduling conflicts
- Communication failures
- Data validation errors
- System recovery

## 📞 Support

For technical support or questions about this implementation:
- Review the code comments for detailed explanations
- Check the error logs in the Streamlit interface
- Verify sample data integrity
- Ensure all dependencies are installed correctly

## 📝 Project Deliverables

This project fulfills the RagaAI Data Science Intern case study requirements:

1. ✅ **Technical Implementation**: Full-featured scheduling agent
2. ✅ **User Experience**: Intuitive chat interface
3. ✅ **Business Logic**: Smart patient detection and scheduling
4. ✅ **Data Integration**: CSV-based EMR simulation
5. ✅ **Communication**: Email and SMS notifications
6. ✅ **Reporting**: Excel export functionality

---

**Developed for RagaAI Data Science Intern Position**  
*Case Study: AI Scheduling Agent*

This project demonstrates practical AI application in healthcare technology, addressing real-world operational challenges in medical practice management.
