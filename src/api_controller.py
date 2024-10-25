"""Patient API Controller"""

import json
from flask import Flask, request, jsonify
from patient_db import PatientDB



class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)


    """
    TODO:
    Implement the following methods,
    use the self.patient_db object to interact with the database. - DONE!

    Every method in this class should return a JSON response with status code - DONE!
    Status code should be 200 if the operation was successful, - DONE!
    Status code should be 400 if there was a client error, - DONE!
    """

    def create_patient(self):
        # here this gets the patient data from the request
        patient_data = request.json

        try:
            self.patient_db.insert_patient(patient_data)
            return jsonify({"message": "Patient created successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    def get_patients(self):
        try:
            patients = self.patient_db.select_all_patients()
            return jsonify(patients), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    def get_patient(self, patient_id):
        try:
            patient = self.patient_db.select_patient(patient_id)
            return jsonify(patient), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    def update_patient(self, patient_id):
        # Get the patient data from the request
        patient_data = request.json

        try:
            self.patient_db.update_patient(patient_id, patient_data)
            return jsonify({"message": "Patient updated successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    def delete_patient(self, patient_id):
        try:
            self.patient_db.delete_patient(patient_id)
            return jsonify({"message": "Patient deleted successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()


PatientAPIController()
