import sys
import os
import unittest
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from config import Config


class TestConfigMethods(unittest.TestCase):

    validation_schema = project_path+"/resources/validationSchema.yaml"
    bad_yaml = project_path+"/test/resources/badYaml.yaml"

    def test_read_yaml_wrong_path(self):

        '''read_yaml Should return None if the file is not found'''
        result = Config.read_yaml("wrongPath")
        self.assertEqual(result, None)

    def test_read_yaml_right_path(self):

        '''read_yaml Should return a dictionary if the file is found and valid'''
        result = Config.read_yaml(self.validation_schema)
        self.assertIsInstance(result, dict)

    def test_read_yaml_wrong_format(self):

        '''read_yaml Should return None if the file is not a valid yaml'''
        result = Config.read_yaml(self.bad_yaml)
        self.assertEqual(result, None)

    def test_get_config_bad_config(self):

        '''get_config should return None if the config file doesnt respect the schema'''
        test_config_not_ok = Config(project_path+"/test/resources/configNotOk.yaml", self.validation_schema)
        result = test_config_not_ok.data
        self.assertEqual(result, None)

    def test_get_config_right_config(self):
        '''get_config should return a dictionary if the config file respect the schema'''
        test_config_ok = Config(project_path+"/test/resources/configOk.yaml", self.validation_schema)
        result = test_config_ok.data
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()