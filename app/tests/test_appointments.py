import sys
import os
import pytest
from datetime import datetime

# Fix the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.database import db  # Import db from database.py
from app.models import Customer, Appointment

@pytest.fixture
def client():
    app = create_app(config_object='test_config.TestConfig')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables for the test
        yield client
        with app.app_context():
            db.drop_all()  # Drop all tables after the test

def test_add_appointment(client):
    # Convert the date string to a Python date object
    appointment_date = datetime.strptime('2024-09-01', '%Y-%m-%d').date()

    # Convert the time string to a Python time object
    appointment_time = datetime.strptime('13:14:00', '%H:%M:%S').time()

    # Make the POST request to add an appointment
    response = client.post('/appointment/add', data={
        'customer_name': 'John zaza',
        'phone_number': '1234567890',
        'date': appointment_date,
        'time': appointment_time,
        'brand': 'Toyota',
        'model': 'Corolla'
    })

    # Assert that the initial response is a redirect
    assert response.status_code == 302

    # Follow the redirect to the appointment list
    response = client.get('/appointments')
    assert response.status_code == 200

    # Check for the flash message on the redirected page
    assert b'New appointment successfully created!' in response.data

    # Check if the appointment was added to the database
    appointment = Appointment.query.first()
    assert appointment is not None
    assert appointment.brand == 'Toyota'
    print(response.data)
