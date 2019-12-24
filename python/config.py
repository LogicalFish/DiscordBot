import os
import yaml

BASEDIR = os.path.dirname(os.path.abspath(__file__))

configuration = yaml.safe_load(open("settings.yaml"))
localization_file = os.path.sep.join(configuration['dir']['localization'])
localization = yaml.safe_load(open(localization_file, encoding="utf8"))
