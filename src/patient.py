"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.
"""

import uuid
import requests
from datetime import datetime

from src.config import DOCTORS, GENDERS, WARD_NUMBERS, ROOM_NUMBERS
from src.patient_db_config import PATIENTS_TABLE, ENGINE
from patient_db import PatientDB



class Patient:

    def __init__(self, name, gender, age):

        self._validate_input(name, gender, age)

        self.id = str(uuid.uuid4())
        self.name = name
        self.gender = gender
        self.age = age
        self.checkin = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.checkout = None
        self.room = None
        self.ward = None


    def _validate_input(self, name, gender, age):

        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        if gender not in GENDERS:
            raise ValueError(f"Gender must be one of {', '.join(GENDERS)}")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer")

    def update_room_and_ward(self, room, ward):

        if not room or not isinstance(room, int):
            raise ValueError("Room number must be a non-empty integer")
        if not ward or not isinstance(ward, int):
            raise ValueError("Ward name must be a non-empty integer")

        if ward not in WARD_NUMBERS:
            raise ValueError(f"Ward number must be one of {WARD_NUMBERS}")

        # Ensure room number is valid for the given ward
        valid_rooms = ROOM_NUMBERS.get(ward)
        if not valid_rooms or room not in valid_rooms:
            raise ValueError(f"Invalid room number for ward {ward}. Available rooms: {', '.join(valid_rooms)}")

        self.room = room
        self.ward = ward

    def commit_to_database(self):

        patient_data = {
            "patient_id": self.id,
            "patient_name": self.name,
            "patient_age": self.age,
            "patient_gender": self.gender,
            "patient_checkin": self.checkin,
            "patient_checkout": self.checkout,
            "patient_ward": self.ward,
            "patient_room": self.room,
        }

        try:
            # Make a POST request to the Flask API endpoint
            response = requests.post("http://localhost:5000/patients", json=patient_data)

            if response.status_code == 200:
                print(f"Patient data for {self.name} committed to database successfully!")
            else:
                print(f"Error occurred while committing patient data: {response.json()['message']}")
        except requests.RequestException as e:
            print(f"Error occurred while committing patient data: {e}")





"""
The attributes for this class should be the same as the columns in the PATIENTS_TABLE. - DONE

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class. - DONE

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time. - DONE

There should be a method to update the patient's room and ward. validation should be used.(config is given) - DONE

Validation should be done for all of the variables in config and db_config. - DONE

There should be a method to commit that patient to the database using the api_controller. - DONE
"""