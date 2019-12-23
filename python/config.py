import os
import yaml

configuration = yaml.safe_load(open("settings.yml"))

# Directories and Files
DB_INI = os.path.sep.join(configuration['dir']['database_file'])
ERRORS = os.path.sep.join(configuration['dir']['errors'])
