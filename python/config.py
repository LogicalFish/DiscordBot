import os
import yaml

configuration = yaml.safe_load(open("settings.yml"))

# Directories and Files
BASEDIR = os.path.dirname(os.path.abspath(__file__))
DB_INI = os.path.sep.join(configuration['dir']['database_file'])
ERRORS = os.path.sep.join(configuration['dir']['errors'])
