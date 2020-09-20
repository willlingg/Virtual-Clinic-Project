import psycopg2
from psycopg2 import pool
import logging
from app.dao.db import Db

class PatientDAO:

    def __init__(self):
        pass

    def __del__(self):
        pass   

    '''
        This method gets the patient details
    
        Parameters: 
            pool:       connection pool object
            patient_id: the unique identifier for the patient being searched

        Return: 
            if the patient was found 
                list containing the patient details
            else if the query failed
                return -1        
    '''
    def get_patient(self, pool, patient_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor()
            
            cur.execute("SELECT patient_id, first_name, middle_name, last_name \
                        from patients where patient_id = %s", (patient_id,))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()
