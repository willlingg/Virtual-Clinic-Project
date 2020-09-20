import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from datetime import date, datetime, timedelta
from app.dao.db import Db

class DocumentDAO:

    def __init__(self):
        pass

    def __del__(self):
        pass

    '''
        This method inserts a new document for a patient
    
        Parameters: 
            pool:       connection pool object
            data:       data consists of the following json key/value pairs

        return: 
            if the insert was successful 
                return 1
            else if the insert failed
                return -1        
    '''
    def insert_patient_document(self, pool, data):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
    
            q = "insert into patient_documents (patient_id, description, file_name, document_type_id) \
                values (%(patient_id)s, %(description)s, %(file_name)s, %(document_type_id)s)"   
            
            #add the new record
            cur.execute(q, data)

            conn.commit()

            return 1

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()

    '''
        This method deletes a document
    
        Parameters: 
            pool:           connection pool object
            pocument_id:    the unique identifier for the document to delete
            
        Return: 
            if the query was successful 
                return 1
            else if the query failed
                return -1        
    '''
    def delete_document(self, pool, document_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor()
            
            # delete the document
            cur.execute('delete from patient_documents where document_id = %s', (document_id,) )

            conn.commit()

            return 1

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()    

    '''
        This method gets a list of all documents related to a patient
    
        Parameters: 
            pool:          connection pool object
            patient_id:    the unique identifier for the patient
            
        Return: 
            if there are documents to return
                list of documents for the patient 
                - document_id, patient_id, description, file_name (inc path), document_type_id, document_type         
            else if there are no documents
                empty list
            else query failed
                return -1  
    '''
    def get_documents_for_patient(self, pool, patient_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("SELECT d.document_id, d.patient_id, d.description, d.file_name, \
                        d.document_type_id, dt.document_type \
                        from patient_documents d left join document_type dt on d.document_type_id = dt.document_type_id \
                        where patient_id = %s", (patient_id,))

            result = cur.fetchall()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()    

    '''
        This method gets the patient id and file_name from the document_id
    
        Parameters: 
            pool:          connection pool object
            document_id:   the unique identifier for the document
            
        Return: 
            if there is a record to return
                tuple containing patient_id, file_name                  
            else if there are no records
                None
            else query failed
                return -1  
    '''
    def get_file_details_from_document_id(self, pool, document_id):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor()
            
            cur.execute("SELECT patient_id, file_name from patient_documents where document_id = %s", (document_id,))

            result = cur.fetchall()

            if len(result) > 0:
                return result[0]
            else:
                return None

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return -1
        finally:
            if conn:
                pool.putconn(conn)
            if cur is not None:
                cur.close()
