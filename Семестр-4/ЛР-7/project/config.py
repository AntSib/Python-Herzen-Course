import os


class Configuration(object):
    SQLALCHEMY_DATABASE_URI = f"{os.path.join('sqlite:///', '<Whatever_path_you_want>', 'db', 'logtable.db')}"
    SERVER_NAME = 'localhost:8080'
