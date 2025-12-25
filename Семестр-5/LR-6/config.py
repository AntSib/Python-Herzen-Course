# import os
import pathlib


class Configuration:
    SQLALCHEMY_DATABASE_URI = (f"sqlite:///{pathlib.Path(__file__).parent.absolute()}/db/logtable.db")
    DEBUG = True
    SERVER_NAME = "localhost:8080"
