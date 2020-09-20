import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import logging
from app.dao.db import Db

class ReferenceDAO:

    def __init__(self):
        pass

    def __del__(self):
        pass

    '''
        Method to get the list of services
        
        Parameters: 
            pool:           conection pool object
        return: 
            if there are services to return
                list of services          
            else if there are no services
                empty list
            else query failed
                return -1   
    '''
    def get_services(self, pool):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("select service_id, service, price from service order by sort_order")

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
        Method to get the list of document types
        
        Parameters: 
            pool:           conection pool object
        return: 
            if there are document types to return
                list of document types          
            else if there are no document types
                empty list
            else query failed
                return -1   
    '''
    def get_document_types(self, pool):
        try:       
            # get connection and create a cursor
            conn = pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("select document_type_id, document_type, sort_order from document_type order by sort_order")

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
          
