import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from datetime import date, datetime, timedelta
import logging
from app.dao.db import Db

class AppointmentDAO:

    def __init__(self):
        pass

    def __del__(self):
        pass

    '''
        Method to get the list of appointments for the selected date
        Returns all appointments for all doctors
        
        Parameters: 
            pool:           conection pool object
            diary_date:     the date of the appointments
        return: 
            if there are appointments to return
                list of appointments for the specified date          
            else if there are no appointments
                empty list
            else query failed
                return -1   
    '''
    def get_appointments_by_date(self, pool, diary_date):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("select dr.doctor_id, dr.first_name, dr.middle_name, dr.last_name, \
                        p.patient_id, p.first_name, p.middle_name, p.last_name, p.phone, \
                        d.diary_id, d.diary_date, ts.time_from, ts.time_to, apt.notes, apt.start_url, apt.join_url \
                        from appointments apt inner join patients p on apt.patient_id = p.patient_id \
                        inner join diary d on apt.diary_id = d.diary_id \
                        inner join doctors dr on d.doctor_id = dr.doctor_id \
                        inner join time_slot ts on d.time_slot_id = ts.time_slot_id \
                        where d.diary_date = %s \
                        order by dr.first_name, dr.last_name, ts.time_from", (diary_date))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        Method to get the list of current appointments for the number of days in advance (includes current day)
        Returns all appointments for all doctors for x number of days in advance
        
        Parameters: 
            pool:     conection pool object
            days:     the date of the appointments
        return: 
            if there are appointments to return
                list of appointments for the specified number of days in advance          
            else if there are no appointments
                empty list
            else query failed
                return -1   
    '''
    def get_appointments_current_days(self, pool, no_days):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            date_to = date.today() + timedelta(days=no_days+1)

            cur.execute("select dr.doctor_id, dr.first_name, dr.middle_name, dr.last_name, \
                        p.patient_id, p.first_name, p.middle_name, p.last_name, p.phone, \
                        d.diary_id, d.diary_date, ts.time_from, ts.time_to, apt.notes, apt.start_url, apt.join_url \
                        from appointments apt inner join patients p on apt.patient_id = p.patient_id \
                        inner join diary d on apt.diary_id = d.diary_id \
                        inner join doctors dr on d.doctor_id = dr.doctor_id \
                        inner join time_slot ts on d.time_slot_id = ts.time_slot_id \
                        where d.diary_date >= %s and d.diary_date < %s \
                        order by dr.first_name, dr.last_name, ts.time_from", (date.today(), date_to))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()

    '''
        Method to get the list of appointments for the selected patient
        Returns all appointments for the patient
        
        Parameters: 
            pool:           conection pool object
            patient_id:     the id of the patient
        return: 
            if there are appointments to return
                list of appointments for the specified patient          
            else if there are no appointments
                empty list
            else query failed
                return -1    
    '''
    def get_appointments_current_by_patient(self, pool, patient_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("select dr.doctor_id, dr.first_name, dr.middle_name, dr.last_name, \
                        p.patient_id, p.first_name, p.middle_name, p.last_name, p.phone, \
                        d.diary_id, d.diary_date, ts.time_from, ts.time_to, apt.notes, apt.start_url, apt.join_url \
                        from appointments apt inner join patients p on apt.patient_id = p.patient_id \
                        inner join diary d on apt.diary_id = d.diary_id \
                        inner join doctors dr on d.doctor_id = dr.doctor_id \
                        inner join time_slot ts on d.time_slot_id = ts.time_slot_id \
                        where p.patient_id = %s and d.diary_date >= %s \
                        order by dr.first_name, dr.last_name, ts.time_from", (patient_id, date.today()))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        Method to get the list of appointments for the selected patient and date
        Returns all appointments for the patient on the selected date
        
        Parameters: 
            pool:           conection pool object
            patient_id:     the id of the patient
        return: 
            if there are appointments to return
                list of appointments for the specified patient          
            else if there are no appointments
                empty list
            else query failed
                return -1   
    '''
    def get_appointments_by_patient_date(self, pool, patient_id, diary_date):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("select dr.doctor_id, dr.first_name, dr.middle_name, dr.last_name, \
                        p.patient_id, p.first_name, p.middle_name, p.last_name, p.phone, \
                        d.diary_id, d.diary_date, ts.time_from, ts.time_to, apt.notes, apt.start_url, apt.join_url \
                        from appointments apt inner join patients p on apt.patient_id = p.patient_id \
                        inner join diary d on apt.diary_id = d.diary_id \
                        inner join doctors dr on d.doctor_id = dr.doctor_id \
                        inner join time_slot ts on d.time_slot_id = ts.time_slot_id \
                        where p.patient_id = %s and d.diary_date = %s \
                        order by dr.first_name, dr.last_name, ts.time_from", (patient_id, diary_date))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        Method to get the list of appointments for the selected doctor and date
        Returns all appointments for the doctor on the selected date
        
        Parameters: 
            pool:           conection pool object
            patient_id:     the id of the doctor
        return: 
            if there are appointments to return
                list of appointments for the specified doctor          
            else if there are no appointments
                empty list
            else query failed
                return -1   
    '''
    def get_appointments_by_doctor_date(self, pool, doctor_id, diary_date):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("select dr.doctor_id, dr.first_name, dr.middle_name, dr.last_name, \
                        p.patient_id, p.first_name, p.middle_name, p.last_name, p.phone, \
                        d.diary_id, d.diary_date, ts.time_from, ts.time_to, apt.notes, apt.start_url, apt.join_url \
                        from appointments apt inner join patients p on apt.patient_id = p.patient_id \
                        inner join diary d on apt.diary_id = d.diary_id \
                        inner join doctors dr on d.doctor_id = dr.doctor_id \
                        inner join time_slot ts on d.time_slot_id = ts.time_slot_id \
                        where dr.doctor_id = %s and d.diary_date = %s \
                        order by dr.first_name, dr.last_name, ts.time_from", (doctor_id, diary_date))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        Method to get the list of current appointments for the number of days in advance (includes current day)
        for a specific doctor
        Returns all appointments for the specific doctor for x number of days in advance
        
        Parameters: 
            pool:     conection pool object
            doctor_id: the unique identifier for the doctor
            days:     the number of days in advance
        return: 
            if there are appointments to return
                list of appointments for the specified doctor and number of days in advance          
            else if there are no appointments
                empty list
            else query failed
                return -1   
    '''
    def get_appointments_current_doctor_days(self, pool, doctor_id, no_days):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            date_to = date.today() + timedelta(days=no_days+1)

            cur.execute("select dr.doctor_id, dr.first_name, dr.middle_name, dr.last_name, \
                        p.patient_id, p.first_name, p.middle_name, p.last_name, p.phone, \
                        d.diary_id, d.diary_date, ts.time_from, ts.time_to, apt.notes, apt.start_url, apt.join_url \
                        from appointments apt inner join patients p on apt.patient_id = p.patient_id \
                        inner join diary d on apt.diary_id = d.diary_id \
                        inner join doctors dr on d.doctor_id = dr.doctor_id \
                        inner join time_slot ts on d.time_slot_id = ts.time_slot_id \
                        where dr.doctor_id = %s and d.diary_date >= %s and d.diary_date < %s \
                        order by dr.first_name, dr.last_name, ts.time_from", (doctor_id, date.today(), date_to))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        This method inserts a new appointment and updates the diary entry to available = N
        so it cannot be used for any other appointment
    
        Parameters: 
            pool:     conection pool object
            data:     dictionary containing appointment details
        return: 
            if the insert was successful 
                return 1
            else if the insert failed
                return -1        
    '''
    def insert_appointment(self, pool, data):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            conn.autocommit = False
            cur = conn.cursor(cursor_factory=RealDictCursor)
    
            q = "insert into appointments (patient_id, diary_id, service_id, \
                start_url, join_url, amount_paid, paid_date, notes) \
                values (%(patient_id)s, %(diary_id)s, %(service_id)s, %(start_url)s, \
                %(join_url)s, %(amount_paid)s, %(paid_date)s, %(notes)s) returning diary_id"   
            
            #add the new record
            cur.execute(q, data)
            diary_id = cur.fetchone()['diary_id']

            # update the diary entry to available = N so it cannot be re-used
            cur.execute("update diary set available = 'N' where diary_id = %s", (diary_id,)) 
            
            conn.commit()

            return 1

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        This method deletes an appointment and updates the diary entry to available = Y
        so it can be used for another appointment
    
        Parameters: 
            pool:           conection pool object
            patient_id:     the patient identifier for the appointment
            diary_id:       the specific diary the appointment is associated with
        return: 
            if the query was successful 
                return 1
            else if the query failed
                return -1        
    '''
    def delete_appointment(self, pool, patient_id, diary_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            conn.autocommit = False
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # delete the appointment
            cur.execute('delete from appointments where patient_id = %s and diary_id = %s returning diary_id', (patient_id, diary_id) )
            diary_id = cur.fetchone()['diary_id']

            # update the diary entry to available = Y so it cannot be re-used
            cur.execute("update diary set available = 'Y' where diary_id = %s", (diary_id,)) 
            
            conn.commit()

            return 1

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        Method to build the start date/time for an diary/ appointment
        Returns the diary date time in the format yyyy-MM-ddTHH:mm:ss
        
        Parameters: 
            pool:     conection pool object
            diary_id: the unique identifier for the diary entry
        return: 
            if the diary entry was found
                the diary date time as a string in the format yyyy-MM-ddTHH:mm:ss          
            else if there are no diary entries found
                None
    '''
    def get_appointment_start_date_time(self, pool, diary_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor()

            cur.execute("select d.diary_date || 'T' || time_from_24 as diary_start_time \
                    from diary d inner join time_slot t on d.time_slot_id = t.time_slot_id \
                    where diary_id = %s", (diary_id, ))

            result = cur.fetchall()[0][0]

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        Method to check if a patient appointment exists
        
        Parameters: 
            pool:     conection pool object
            patient_id: the unique identifier for the patient 
            diary_id: the unique identifier for the diary entry
        return: 
            if the appointment exists
                True       
            else
                False
    '''
    def check_appointment_exists(self, pool, patient_id, diary_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor()

            cur.execute("select count(*) from appointments \
                      where patient_id = %s and diary_id = %s", (patient_id, diary_id))

            result = cur.fetchall()[0][0]

            if result == 1:
                return True
            else:
                return False   

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()

    '''
        To Do
        Update payment for appointment
    '''
    def update_payment(self, pool):
        pass          
