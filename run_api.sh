#!/bin/sh


pip install -r requirements.txt
cd virtual_clinic/api
export FLASK_APP=virtualclinic.py
python -m flask run
