import os


class Configuration(object):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'db', 'logtable.db')}"
    
    DEBUG = True
    SERVER_NAME = 'localhost:8080'
