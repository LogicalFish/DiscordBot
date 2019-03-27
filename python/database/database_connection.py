import psycopg2
from configparser import ConfigParser
import settings


class DatabaseConnection:

    def __init__(self, filename=settings.DB_INI, section='postgresql'):
        self.filename = filename
        self.section = section
        self.conn = self.connect()

    def config(self):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.section, self.filename))

        return db

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # Read connection parameters
            params = self.config()

            # Connect to the database
            print('Connecting to the PostgreSQL database...')
            return psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')
