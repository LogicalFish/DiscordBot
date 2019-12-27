import os
import yaml

BASEDIR = os.path.dirname(os.path.abspath(__file__))

configuration_file = os.path.sep.join([BASEDIR, "settings.yaml"])
configuration = yaml.safe_load(open(configuration_file))
localization_file = os.path.sep.join([BASEDIR] + configuration['dir']['localization'])
localization = yaml.safe_load(open(localization_file, encoding="utf8"))
