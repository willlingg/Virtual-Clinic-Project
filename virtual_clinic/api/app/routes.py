from flask import jsonify, request, abort, send_file, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_restx import Resource
from datetime import datetime
from app import app, api
from app.dao import Db, DoctorDAO, AppointmentDAO, PatientDAO, DocumentDAO
from app.zoom import ZoomAPI
from app.s3 import *
from app.serializers import appointment


db = Db()
doctorDAO = DoctorDAO()
appointmentDAO = AppointmentDAO()
patientDAO = PatientDAO()
documentDAO = DocumentDAO()
zoom = ZoomAPI()
app.config['ERROR_404_HELP'] = False


@api.route('/doctors')
class Doctors(Resource):

    @api.doc(responses={200: 'Success', 404: 'Not Found', 400: 'Validation Error'})
    def get(self):
        """
        Returns JSON of all doctors in database
        """
        return make_response(jsonify(doctorDAO.get_doctors(db.con_pool)), 200)


@api.route('/diary/<int:doctor_id>/<string:date>')
class Diaries(Resource):

    @api.doc(params={'doctor_id': 'Unique Identifier for a Doctor', 'date' : 'YYYY-MM-DD'})
    @api.doc(responses={200: 'Success', 404: 'Not Found', 400: 'Validation Error'})
    def get(self, doctor_id, date):
        """
        Returns JSON of diary for a particular doctor on a certain date
        """
        if not doctorDAO.get_doctor_by_id(db.con_pool, doctor_id):
            abort(404, 'Doctor id not found')

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            abort(400, 'Invalid date')

        return make_response(jsonify(
            doctorDAO.get_doctor_diary_by_day(db.con_pool, doctor_id, date)), 200)


appointment_namespace = api.namespace('appointment', description='Operations for patients and doctors to create, retrieve and delete appointments.')

@appointment_namespace.route('')
class Appointments(Resource):

    @appointment_namespace.expect(appointment)
    @appointment_namespace.doc(responses={201: 'Success', 404: 'Not Found', 400: 'Validation Error', 500: 'Internal Server Error'})
    def post(self):
        """
        Inserts an appointment into the backend database
        """
        if request.json is None:
            abort(400, 'Request must be in JSON format')

        patient_id, diary_id = request.json.get('patient_id'), request.json.get('diary_id')
        if not patient_id or not diary_id:
            abort(400, 'Invalid request')

        start_time = appointmentDAO.get_appointment_start_date_time(db.con_pool, diary_id)
        if start_time == -1:
            abort(404, 'Diary id not found')

        patient_data = patientDAO.get_patient(db.con_pool, patient_id)
        if not patient_data:
            abort(404, 'Patient id not found')

        if appointmentDAO.check_appointment_exists(db.con_pool, patient_id, diary_id):
            abort(400, 'Appointment already exists')

        patient_name = ' '.join(filter(None, patient_data[1:]))
        start_url, join_url = zoom.create_zoom_meeting(
            start_time, 10, 'Virtual Clinic Consultation', f'consultation with {patient_name}', 1209600)
        data = {'patient_id': patient_id, 'diary_id': diary_id, 'service_id': None, 'start_url': start_url,
                'join_url': join_url, 'amount_paid': None, 'paid_date': None, 'notes': None}
        if appointmentDAO.insert_appointment(db.con_pool, data) != 1:
            abort(500)

        return {'patient_id': patient_id, 'diary_id': diary_id}, 201


    @appointment_namespace.expect(appointment)
    @appointment_namespace.doc(responses={200: 'Success', 404: 'Not Found', 400: 'Validation Error', 500: 'Internal Server Error'})
    def delete(self):
        """
        Deletes appointment from backend database.
        """
        if not request.json:
            abort(400, 'Request must be in JSON format')

        patient_id, diary_id = request.json.get('patient_id'), request.json.get('diary_id')
        if not patient_id or not diary_id:
            abort(400, 'Invalid request')

        if not appointmentDAO.check_appointment_exists(db.con_pool, patient_id, diary_id):
            abort(404, 'Appointment does not exist')

        if appointmentDAO.delete_appointment(db.con_pool, patient_id, diary_id) != 1:
            abort(500)

        return {'patient_id': patient_id, 'diary_id': diary_id}, 200


@appointment_namespace.route('/patient/<int:patient_id>')
class PatientAppointments(Resource):

    @appointment_namespace.doc(params={'patient_id' : 'Unique Identifier for a Patient'})
    @appointment_namespace.doc(responses={200: 'Success', 404: 'Not Found'})
    def get(self, patient_id):
        """
        Returns all appointments for a particular patient
        """
        if not patientDAO.get_patient(db.con_pool, patient_id):
            abort(404, 'Patient id not found')

        return make_response(jsonify(
            appointmentDAO.get_appointments_current_by_patient(db.con_pool, patient_id)), 200)


@appointment_namespace.route('/doctor/<int:doctor_id>')
class DoctorAppointments(Resource):

    @appointment_namespace.doc(params={'doctor_id' : 'Unique Identifier for a Doctor'})
    @appointment_namespace.doc(responses={200: 'Success', 404: 'Not Found'})
    def get(self, doctor_id):
        """
        Returns all appointments for particular doctor
        """
        if not doctorDAO.get_doctor_by_id(db.con_pool, doctor_id):
            abort(404, 'Doctor id not found')

        return make_response(jsonify(
            appointmentDAO.get_appointments_current_doctor_days(db.con_pool, doctor_id, 5)), 200)


file_namespace = api.namespace('file', description='Operations for uploading and downloading files through the website.')
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@file_namespace.route('/patient/<int:patient_id>')
class PatientDocuments(Resource):

    @file_namespace.expect(upload_parser)
    @file_namespace.doc(params={'patient_id' : 'Unique Identifier for a Patient'})
    @file_namespace.doc(responses={201: 'Success', 404: 'Not Found', 400: 'Validation Error', 500: 'Internal Server Error'})
    def post(self, patient_id):
        """
        Uploads document to database for a particular patient
        """
        if not patientDAO.get_patient(db.con_pool, patient_id):
            abort(404, 'Patient id not found')

        file = request.files.get('file')
        if not file or file.filename == '':
            abort(400, 'Missing file')

        if not allowed_file_extension(file.filename):
            abort(400, f"Invalid file type. Accepted file types are: {', '.join(app.config['UPLOAD_EXTENSIONS'])}")

        filename = secure_filename(file.filename)
        if check_file_exists(patient_id, filename):
            abort(400, 'File already exists')

        description = request.form.get('description')
        document_type_id = request.form.get('document_type_id')
        data = {'patient_id': patient_id, 'description': description,
                'file_name': filename, 'document_type_id': document_type_id}
        if (not save_file(file, patient_id, filename) or
                not documentDAO.insert_patient_document(db.con_pool, data)):
            abort(500)

        return 'File successfully uploaded', 201


    @file_namespace.doc(params={'patient_id' : 'Unique Identifier for a Patient'})
    @file_namespace.doc(responses={200: 'Success', 404: 'Not Found'})
    def get(self, patient_id):
        """
        Returns JSON of documents for a patient
        """
        if not patientDAO.get_patient(db.con_pool, patient_id):
            abort(404, 'Patient id not found')

        return make_response(jsonify(
            documentDAO.get_documents_for_patient(db.con_pool, patient_id)), 200)


@file_namespace.route('/<int:document_id>')
class Documents(Resource):

    @file_namespace.doc(params={'document_id' : 'Unique Identifier for a Document'})
    @file_namespace.doc(responses={200: 'Success', 404: 'Not Found'})
    def get(self, document_id):
        """
        Returns download link to a particular file
        """
        file_details = documentDAO.get_file_details_from_document_id(db.con_pool, document_id)
        if not file_details:
            abort(404, 'Document id not found')

        patient_id, filename = file_details
        file = download_file(patient_id, filename)
        return send_file(file, attachment_filename=filename)


    @file_namespace.doc(params={'document_id' : 'Unique Identifier for a Document'})
    @file_namespace.doc(responses={200: 'Success', 404: 'Not Found', 500: 'Internal Server Error'})
    def delete(self, document_id):
        """
        Deletes document from database
        """
        file_details = documentDAO.get_file_details_from_document_id(db.con_pool, document_id)
        if not file_details:
            abort(404, 'Document id not found')

        patient_id, filename = file_details
        if (not delete_file(patient_id, filename) or
                not documentDAO.delete_document(db.con_pool, document_id)):
            abort(500)

        return {'document_id': document_id}, 200
