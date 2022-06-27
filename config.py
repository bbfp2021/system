import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-my-key'
    SQLALCHEMY_DATABASE_URI = 'mysql://bbfp:bbfp123@localhost/bbfp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False #To be changed to true in future
    
    EMULATOR_MODE = True