import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    '''
        Set config variables for the flask app
        Using Environment variables where available.
        Otherwise create the config variable if not done already
    '''

    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Akuma is the true master of the fist'
    # Update the SQLALCHEMY_DATABASE_URI to use the new ElephantSQL URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://mducrmnm:jAhgfltCQsXKaD4it_Q3eMz9weOsy4bV@stampy.db.elephantsql.com/mducrmnm'
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
