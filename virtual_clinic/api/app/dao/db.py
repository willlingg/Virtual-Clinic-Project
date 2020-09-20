import psycopg2
from configparser import ConfigParser
from psycopg2.pool import SimpleConnectionPool
import os
import logging

class Db:

    '''
        The constructor method when the object is instantiated
        Read the database configuration file for required parameters 
    '''
    def __init__(self):
        db_params = self.read_config("database.ini", "postgresql")
        pool_params = self.read_config("database.ini", "pool")
        self.con_pool = psycopg2.pool.SimpleConnectionPool(pool_params['min'], pool_params['max'], **db_params)

    '''
        The destructor method closes all of the database connections and pool
    '''
    def __del__(self):
        if (self.con_pool):
            self.con_pool.closeall
            logging.info("Database Connections Closed")

    '''
        This method reads the database configuration file 
        
        Parameters:
            filename:   the name of the configuration file
            section:    the section to start reading from
            
        Return:
            the parameters read fromthe configuration file
    '''
    def read_config(self, filename, section):
        # create a parser
        parser = ConfigParser()
        # read config file
        file = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.isfile(file):
            raise Exception('{1} file not found'.format(section, filename))
        parser.read(file)
    
        # get section
        prm = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                prm[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))            
    
        return prm
