import psycopg2
from configparser import ConfigParser
import settings
from database.database_error import DatabaseError


class DatabaseConnection:
    """
    Class that maintains a connection with a database.
    """

    def __init__(self, filename=settings.DB_INI, section='postgresql'):
        """Initializes the instance."""
        self.filename = filename
        self.section = section
        self.conn = self.connect()

    def config(self):
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

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # Read connection parameters
            params = self.config()

            # Connect to the database
            print('Connecting to the PostgreSQL database...')
            return psycopg2.connect(**params)

        except (DatabaseError, psycopg2.DatabaseError) as error:
            # raise DatabaseError(error)
            print(error)

    def close_connection(self):
        """Close the database connection."""
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')
