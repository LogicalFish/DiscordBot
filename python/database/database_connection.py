from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

import config

Base = declarative_base()


class DatabaseConnection:

    def __init__(self, filename=config.DB_INI, section='new_post'):
        self.filename = filename
        self.section = section
        print('Connecting to the PostgreSQL database...')
        config_url = self.get_url_from_config_dict(self.get_config_params())
        # Connect to the database
        try:
            self.engine = create_engine(config_url)
            self.engine.connect()
        except OperationalError:
            print('No database found. Database functionality disabled.')
            self.engine = None

    def get_config_params(self,):
        """ Read the .ini file and get configurations."""
        # Create a parser
        parser = ConfigParser()
        # Read config file
        parser.read(self.filename)

        # Get section
        database_parameters = {}
        if parser.has_section(self.section):
            ini_params = parser.items(self.section)
            for param in ini_params:
                database_parameters[param[0]] = param[1]
        else:
            raise DatabaseError('Section {0} not found in the {1} file'.format(self.section, self.filename))

        return database_parameters

    @staticmethod
    def get_url_from_config_dict(config_dict):
        config_url = "{0}://{1}:{2}@{3}:{4}/{5}".format(config_dict["drivername"],
                                                        config_dict["username"],
                                                        config_dict["password"],
                                                        config_dict["host"],
                                                        config_dict["port"],
                                                        config_dict["database"])
        return config_url


class DatabaseError(Exception):
    """
    Special Error Class, to be thrown when the database can't be initialized correctly.
    """

    def __init__(self, error_type):
        super().__init__(error_type)
        self.type = error_type

    def __str__(self):
        return self.type
