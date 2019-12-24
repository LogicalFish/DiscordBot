import os
from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from config import configuration, BASEDIR
from database import Base
from database.models import models


class DatabaseConnection:

    def __init__(self):
        self.filename = os.path.sep.join([BASEDIR] + configuration['database']['ini_file'])
        self.section = configuration['database']['db_section']
        print('Connecting to the {} database...'.format(self.section))
        # Connect to the database
        try:
            config_url = self.get_url_from_config_dict(self.get_config_params())
            self.engine = create_engine(config_url)
            self.engine.connect()
            Base.metadata.create_all(self.engine, checkfirst=True)
        except OperationalError:
            raise DatabaseError("Database not found.")

    def get_config_params(self):
        """ Read the .ini file and get configurations."""
        # Create a parser
        parser = ConfigParser()
        # Read config file
        if not os.path.isfile(self.filename):
            raise DatabaseError('No file {0} found.'.format(self.filename))
        parser.read(self.filename)

        # Get section
        database_parameters = {}
        if parser.has_section(self.section):
            ini_params = parser.items(self.section)
            for param in ini_params:
                database_parameters[param[0]] = param[1]
        else:
            raise DatabaseError('Section [{0}] not found in the {1} file.'.format(self.section, self.filename))

        return database_parameters

    def get_url_from_config_dict(self, config_dict):
        if "drivername" not in config_dict:
            raise DatabaseError("No valid drivername found in section [{0}] of the {1} file.".format(self.section,
                                                                                                     self.filename))
        port = ":{}".format(config_dict["port"]) if "port" in config_dict else ""
        config_url = "{driver}://{user}:{password}@{host}{port}/{db}".format(driver=config_dict["drivername"],
                                                                             user=config_dict.get("username", ""),
                                                                             password=config_dict.get("password", ""),
                                                                             host=config_dict.get("host", ""),
                                                                             port=port,
                                                                             db=config_dict.get("database", ""))
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
