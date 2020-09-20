import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import logging
from app.dao.db import Db

class DoctorDAO:

    def __init__(self):
        pass

    def __del__(self):
        pass

    '''
    Method to get the list of doctors
    
    Parameters:
        pool:       connection pool object
    
    Return:
        a list of doctors, each doctor detail are contained in a tuple 
    '''
    def get_doctors(self, pool):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("SELECT doctor_id, first_name, middle_name, last_name \
                        from doctors order by first_name, last_name")

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()

    '''
    Method to get a doctor base on name
    
    Parameters:
        pool:       connection pool object
        doctor_id:  unique identifier for a doctor
        
    Return:
        a list of doctors, each doctor detail are contained in a tuple
    '''
    def get_doctor_by_id(self, pool, doctor_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("SELECT doctor_id, first_name, middle_name, last_name \
                        from doctors where doctor_id = %s", (doctor_id,))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
    Method to get the diary entries for a doctor for the date + 6 days
    
    Parameters:
        pool:       connection pool object
        doctor_id:  unique identifier for the doctor
        date_from:  the start date for the diary entries
        
    Return:
        the doctor's diary for a week from the date selected
    '''
    def get_doctor_diary_by_week(self, pool, doctor_id, date_from):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("select d.diary_id, d.doctor_id, d.diary_date, \
                t.time_slot, t.time_from, t.time_to, d.time_slot_id, d.available, d.notes \
                from diary d inner join time_slot t on d.time_slot_id = t.time_slot_id \
                where d.doctor_id = %s and d.diary_date between %s::timestamp and %s::timestamp + '6 days'::interval", (doctor_id, date_from, date_from,))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()

    '''
    Method to get the diary entries for a doctor for a specific date
    
    Parameters:
        pool:       connection pool object
        doctor_id:  the identifier for the doctor whose diary entries are to be returned
        diary_date: the date on which the diary entries are to be returned
        
    Return:
        the doctor's diary for the selected date
    '''
    def get_doctor_diary_by_day(self, pool, doctor_id, diary_date):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("select d.diary_id, d.doctor_id, d.diary_date, \
                t.time_slot, t.time_from, t.time_to, d.time_slot_id, d.available, d.notes \
                from diary d inner join time_slot t on d.time_slot_id = t.time_slot_id \
                where d.doctor_id = %s and d.diary_date = %s", (doctor_id, diary_date, ))

            result = cur.fetchall()
            
            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()


    '''
        This method updates the diary entry for a doctor
        
        Parameters: 
            pool:       connection pool object
            diary_id:   the id of the diary entry
            available:  flag to indicate if the diary time slot is available ('y', 'n')
            notes:      any notes regarding this diary entry
            
        Return:
            if update was successful:   
                1
            else:
                -1
    '''
    def update_diary(self, pool, diary_id, available, notes):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # update the location confidence based on the decay weight from the object class           
            cur.execute("update diary set available = %s, notes = %s \
                    where diary_id = %s", (available, notes, diary_id),)  
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
        This method updates the diary availability for a doctor
        
        Parameters: 
            pool:       conection pool object
            diary_id:   the id of the diary entry
            available:  flag to indicate if the diary time slot is available ('y', 'n')
            
        Return:
            if update was successful:   
                1
            else:
                -1
    '''
    def update_diary_availability(self, pool, diary_id, available):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # update the location confidence based on the decay weight from the object class           
            cur.execute("update diary set available = %s \
                    where diary_id = %s", (available, diary_id),)  
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
        This method updates the notes in the diary entry for a doctor
        
        Parameters: 
            pool:       conection pool object
            diary_id:   the id of the diary entry
            notes:      any notes regarding this diary entry
            
        Return:
            if update was successful:   
                1
            else:
                -1
    '''
    def update_diary_notes(self, pool, diary_id, notes):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # update the location confidence based on the decay weight from the object class           
            cur.execute("update diary set notes = %s \
                    where diary_id = %s", (notes, diary_id),)  
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
