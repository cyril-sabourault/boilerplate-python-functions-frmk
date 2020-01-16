import logging
import sys
import yaml


class Config:
    """
    This class manages configuration values.
    """
    _data = None

    def __init__(self, *args, **kwargs):
        file_path = kwargs.get('config_path', 'config.yaml')
        self._data = self.load_from_file(file_path)

    def get(self, key):
        path = key.split('.')
        current_value = self._data

        try:
            for _ in path:
                current_value = current_value[_]
        except (KeyError, TypeError):
            logging.error('Missing config value for key: {}'.format(key))
            sys.exit(1)

        return current_value

    @classmethod
    def load_from_file(cls, file_path):
        try:
            with open(file_path, 'r') as fd:
                config = yaml.load(fd, Loader=yaml.FullLoader)
                return config
        except yaml.YAMLError as exc:
            logging.error('Error in configuration file: {}'.format(exc))
            sys.exit(1)
        except OSError:
            logging.error('{} config file can\'t be found'.format(file_path))
            sys.exit(1)
