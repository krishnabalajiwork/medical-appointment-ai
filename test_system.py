"""
Test script for Medical Appointment Scheduling AI Agent
Run this to verify the system is working correctly
"""
import sys
import pandas as pd
from datetime import datetime
import os

def test_data_files():
    """Test if all required data files exist and are valid"""
    print("Testing data files...")

    required_files = ['patients.csv', 'doctors.csv', 'schedules.csv']

    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing file: {file}")
            return False
        else:
            print(f"✅ Found: {file}")

    # Test data loading
    try:
        patients_df = pd.read_csv('patients.csv')
        doctors_df = pd.read_csv('doctors.csv')
        schedules_df = pd.read_csv('schedules.csv')

        print(f"✅ Loaded {len(patients_df)} patients")
        print(f"✅ Loaded {len(doctors_df)} doctors")
        print(f"✅ Loaded {len(schedules_df)} schedule slots")

        return True
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_imports():
    """Test if all modules can be imported"""
    print("\nTesting module imports...")

    try:
        from patient_agent import PatientAgent
        print("✅ PatientAgent imported successfully")

        from database import PatientDatabase
        print("✅ PatientDatabase imported successfully")

        from scheduler import SmartScheduler
        print("✅ SmartScheduler imported successfully")

        from communication import CommunicationManager
        print("✅ CommunicationManager imported successfully")

        from utils import validate_email
        print("✅ Utils imported successfully")

        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic system functionality"""
    print("\nTesting basic functionality...")

    try:
        from patient_agent import PatientAgent
        from database import PatientDatabase

        # Test database
        db = PatientDatabase()
        patient = db.find_patient(name="John Smith")
        print(f"✅ Database search works: {patient is not None}")

        # Test agent
        agent = PatientAgent()
        response = agent.process_message("Hello")
        print(f"✅ Agent responds: {len(response) > 0}")

        # Test scheduler
        from scheduler import SmartScheduler
        scheduler = SmartScheduler()
        slots = scheduler.get_available_appointments("Dr. Smith", num_days=7)
        print(f"✅ Scheduler works: {len(slots) > 0} slots found")

        return True
    except Exception as e:
        print(f"❌ Functionality error: {e}")
        return False

def test_streamlit_requirements():
    """Test if Streamlit and required packages are available"""
    print("\nTesting Streamlit requirements...")

    try:
        import streamlit
        print("✅ Streamlit available")

        import pandas
        print("✅ Pandas available")

        import numpy
        print("✅ Numpy available")

        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def main():
    """Run all tests"""
    print("🧪 Medical Appointment Scheduling AI Agent - System Test")
    print("=" * 60)

    tests = [
        test_data_files,
        test_imports,
        test_streamlit_requirements,
        test_basic_functionality
    ]

    results = []

    for test in tests:
        result = test()
        results.append(result)

    print("\n" + "=" * 60)
    print("📊 Test Results:")

    passed = sum(results)
    total = len(results)

    print(f"✅ Passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run main.py")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the issues above.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
