from flask_restx import fields
from app import api

appointment = api.model('Appointment', {
    'patient_id': fields.Integer(readOnly=True, description='Unique identifier for a Patient'),
    'diary_id': fields.Integer(readOnly=True, description='Unique identifier for a Diary')
})
