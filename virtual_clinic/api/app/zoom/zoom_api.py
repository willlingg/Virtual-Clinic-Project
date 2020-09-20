'''
    This class contains all of the methods to create a Zoom Meeting

    Usage:
        zoom = ZoomAPI(api_key, api_secret, email)
        start_url, join_url = create_zoom_meeting('2020-08-15T14:20:00', 20,
            'Patient Consultation', 'Consultation for patient name', 3600)
'''
import json
import time
import jwt
import requests
import os
from configparser import ConfigParser

class ZoomAPI:

    '''
        The constructor sets the initial values for the mandatory authorisation values

        Parameters:
            api_key - the zoom api key taken from the zoom JWT app hosted on zoom marketplace
            api_secret - the zoom api secret taken from the zoom JWT app hosted on zoom marketplace
            user_email - the email address of the user account that created the JWT app
    '''
    def __init__(self):
        zoom_prms = self.read_config("zoom.ini", "zoom")
        self.API_KEY = zoom_prms['api_key']
        self.API_SECRET = zoom_prms['api_secret']
        self.USER_EMAIL = zoom_prms['user_email']
        self.MEETING_ENDPOINT = "https://api.zoom.us/v2/users/" + self.USER_EMAIL + "/meetings"

    '''
        This method reads the config file
        Parameters:
            filename - the name of the ini/coonfig file
            section - the section that contains the relevant
                      key/value parameters
        Return:
            dictionary object with key/value pairs representing parameters
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

    '''
        This is the main method to call when creating the zoom meeting. 
        The post request requires a number of components to pass to the 
        zoom endpoint. Functions to build these components are called from this 
        method.

        Parameters:
            start_time - the start time of the meeting
            meeting_duration - the number of minutes the meeting is scheduled to run
            topic - the meeting subject
            agenda - text describing the meeting
            expiry_time - the number of minutes the token will be valid 
                e.g. 3600 

        Return:
            start_url - the url that allows the host to connect and start the meeting
            join_url - the url for the other participants to join the meeting
    '''
    def create_zoom_meeting(self, start_time, meeting_duration, topic, agenda, expiry_time):
        meeting_request = self.build_meeting_request(start_time, meeting_duration, topic, agenda)
        header = self.create_header(expiry_time)
        r = requests.post(url=self.MEETING_ENDPOINT, headers=header, data=meeting_request)
        start_url, join_url = self.extract_zoom_url(r.text)
        print(r.text)
        return start_url, join_url

    '''
        One of the security requirements when creating a zoom meeting is 
        to add a token. Each meeting will only be valid for a certain time
        and will expire after that time.

        Parameters:
            start_time - the start date and time of the appointment  
            expiry_time - the number of minutes the meeting will be valid

        Return:
             token - the JWT token required by the zoom post method
    '''
    def refresh_token(self, expiry_time):
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"iss": self.API_KEY, "exp": int(time.time() + expiry_time)}
        token = jwt.encode(payload, self.API_SECRET, algorithm="HS256", headers=header)
        return token.decode("utf-8")
      
    '''
        The zoom meeting requies certain header information to be passed to enable the 
        correct creation of the meeting. The header carries the authorisation details

        Parameters:
            expiry_time - the number of minutes the meeting will be valid

        Return:
            header - containing the authorisation details
    '''
    def create_header(self, expiry_time):
        token = self.refresh_token(expiry_time)

        header = {
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/json",
        }
        return header

    '''
        This method builds the meeting request body. The meeting request body 
        contains information such as time of meeting and agenda.

        Parameters:
            topic - title of the meeting
            start_time - the start date and time of the meeting 
                yyyy-MM-ddTHH:mm:ss e.g. 2020-08-06T22:10:00
            meeting_duration - the number of minutes the meeting will run
            agenda - description or agenda for meeting
        Return:
            meeting_request - json string containing meeting details
    '''
    def build_meeting_request(self, start_time, meeting_duration, topic, agenda):
        request = {
            "topic": topic, "type": 2, "start_time": start_time, "duration": meeting_duration,
            "schedule_for": "", "timezone": "Australia/Sydney", "agenda": agenda,
            "settings": {
                "host_video": "True",
                "join_before_host": "True", "mute_upon_entry": "False",
                "registrants_email_notification": "True"
            }
        }
        return json.dumps(request)

    '''
        This method extracts the zoom meeting url from the http response

        Parameters:
            zoom_response - the json string containing the http response
        
        Return:
            zoom_url - the url for the zoom meeting
    '''
    def extract_zoom_url(self, zoom_response):
        zoom = json.loads(zoom_response)
        start_url = zoom["start_url"]
        join_url = zoom["join_url"]
        return start_url, join_url
