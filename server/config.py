from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

class Config(object):
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = int(environ.get("FLASK_DEBUG", default=0))
    SECRET_KEY = environ.get("SECRET_KEY")
    
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")

    API_KEY = environ.get("API_KEY")
    API_VERSION = environ.get("API_VERSION")