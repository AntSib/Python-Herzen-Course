import os


class Configuration(object):
    UPLOAD_FOLDER = 'uploads'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'project', 'db', 'logtable.db')}"
    
    DEBUG = True
    SERVER_NAME = 'localhost:8080'
