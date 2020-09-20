from db import Db
from doctor_dao import DoctorDAO
from reference_dao import ReferenceDAO
from appointment_dao import AppointmentDAO
from patient_dao import PatientDAO

db = Db()               # database connections

# DAO layer
dr_dao = DoctorDAO()
ref_dao = ReferenceDAO()
apt_dao = AppointmentDAO()
ptn_dao = PatientDAO()


# Reference Methods
ref = ref_dao.get_document_types(db.con_pool)
print("Document Types Type: ", type(ref))
print(ref)

ref = ref_dao.get_services(db.con_pool)
print("Services Type: ", type(ref))
print(ref)

# Doctor Methods
dr = dr_dao.get_doctors(db.con_pool)
print("Get Doctors Type: ", type(dr))
print(dr)

dr = dr_dao.get_doctor_by_id(db.con_pool, 2)
print("Get Doctors By Id Type: ", type(dr))
print(dr)

dr_diary = dr_dao.get_doctor_diary_by_week(db.con_pool, 1, '2020-07-22')
print("Get Doctor diary by week Type: ", type(dr_diary))
print(dr_diary)

dr_diary = dr_dao.get_doctor_diary_by_day(db.con_pool, 1, '2020-07-30')
print("Get Doctor diary by day Type: ", type(dr_diary))
print(dr_diary)

dr_diary = dr_dao.update_diary_availability(db.con_pool, 15268, 'N')
print("Update diary availability: ", type(dr_diary))
print(dr_diary)

dr_diary = dr_dao.update_diary_notes(db.con_pool, 15269, 'test notes')
print("Update diary notes: ", type(dr_diary))
print(dr_diary)

dr_diary = dr_dao.update_diary(db.con_pool, 15271, 'N', 'test notes 2')
print("Update diary: ", type(dr_diary))
print(dr_diary)


# Appointment Methods
new_data = {"patient_id":1, "diary_id":15270, "service_id":1, "start_url": "https://zoom.com/1234567890/", "join_url":"https://zoom.com/12345", "amount_paid":None, "paid_date": None,"receipt":None, "notes":"test note"}
apt = apt_dao.insert_appointment(db.con_pool, new_data)
print("insert appointment: ", type(apt))
print(apt)

apt = apt_dao.get_appointments_current_doctor_days(db.con_pool, 2, 5)
print("Get current Dr appointments for days")
print(apt)

# get the date time in correct format for zoom meeting
diary_dt = apt_dao.get_appointment_start_date_time(db.con_pool, 15270)
print(diary_dt)

doc = {"patient_id":1, "description":"Blood test results from last week", "file_name":"/path to file/blood_test.txt", "document_type_id":3}
docs = doc_dao.insert_patient_document(db.con_pool, doc)
print(docs)

result = doc_dao.get_documents_for_patient(db.con_pool, 1)
print(result)

result = doc_dao.delete_document(db.con_pool, 4)

result = doc_dao.get_documents_for_patient(db.con_pool, 1)
print(result)

result = doc_dao.get_file_details_from_document_id(db.con_pool, 5)
print(result)

result = apt_dao.check_appointment_exists(db.con_pool, 1, 15050)
print(result)

result = apt_dao.check_appointment_exists(db.con_pool, 10, 15050)
print(result)
