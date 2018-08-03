import yaml
from cerberus import Validator


class Config(object):

    def __init__(self, path="resources/config.yaml", validation_schema="resources/validationSchema.yaml"):
        """
        :param path: path to the config file
        :param validation_schema: validation schema in yaml format
        """
        self.config_file = path
        self.validation_schema = validation_schema
        self.data = self.get_config()

    def get_config(self):
        """
        Reads the configuration from the config.yaml file and verifies that is compilant with the validation schema
        :return:
        Dictionary with the configuration or None if the config file is invalid
        """
        data = Config.read_yaml(self.config_file)
        schema = Config.read_yaml(self.validation_schema)
        try:
            validator = Validator(schema)
            if validator.validate(data):
                return data
            else:
                return None
        except Exception as e:
            print("ERROR: Exception trying to validate configuration file:" + str(e))

    @staticmethod
    def read_yaml(path):
        """
        Reads a yaml file
        :param path: path to the yaml file
        :return: dictionary with the data or None if fails
        """
        try:
            with open(path) as myFile:
                data = yaml.safe_load(myFile)
            return data
        except Exception as e:
            print("ERROR: Exception loading config file from " + path + "\n" + str(e))
            return None
