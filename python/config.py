import os
import yaml

configuration = yaml.safe_load(open("settings.yaml"))
localization_file = os.path.sep.join(configuration['dir']['localization'])
localization = yaml.safe_load(open(localization_file, encoding="utf8"))
