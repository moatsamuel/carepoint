import os
from dotenv import load_dotenv

load_dotenv()

class GeneralConfig(object):
    APP_NAME = 'CarePoint'
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI ='mysql+mysqlconnector://root@localhost/carepoint'
    SQLALCHEMY_TRACK_MODIFICATIONS = False