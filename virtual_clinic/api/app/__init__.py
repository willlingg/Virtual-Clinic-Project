from flask import Flask
from flask_restx import Api
app = Flask(__name__)
app.config.from_pyfile('s3.cfg')
api = Api(app=app, version="1.0",
          title="Virtual Clinic Flask API",
          description="The core of the API layer for our solution")
from app import routes
