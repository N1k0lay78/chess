import os

SECRET_KEY = os.urandom(30)
DEBUG = False
TESTING = False
UPLOAD_FOLDER = "static/img/"
DATABASE = "db/.sqlite"