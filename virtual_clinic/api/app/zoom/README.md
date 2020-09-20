### Zoom API

In order for the Zoom functionality to work you must have the following:

Zoom Account - can be setup at https://marketplace.zoom.us/

Zoom JWT App - once logged into Zoom Marketplace:

1. Build a JWT app (Develop->Build App menu)

2. Access the credentials 
```
API_KEY
API_SECRET
```
3. Edit the zoom.ini file and copy your credentials in the relevant fields. The zoom.ini file is located in 
```
/virtual-clinic/virtual_clinic/api/app/zoom
```
zoom.ini
```
[zoom]

api_key=xxxxxxxxxxxxxx  (copied from Zoom JWT app)

api_secret=xxxxxxxxxxxxxxxx (copied from Zoom JWT app)

user_email=yyyyyyyyyyyy@gmail.com (email address of your Zoom account)
```
