import configparser
import json
import yaml

class Configs:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = None
        self.file_type = None

    def load(self):
        if self.config_file.endswith('.ini'):
            self.file_type = 'ini'
            self.config = configparser.ConfigParser()
            self.config.read(self.config_file)
        elif self.config_file.endswith('.json'):
            self.file_type = 'json'
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        elif self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
            self.file_type = 'yaml'
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)

    def save(self):
        if self.file_type == 'ini':
            with open(self.config_file, 'w') as f:
                self.config.write(f)
        elif self.file_type == 'json':
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        elif self.file_type == 'yaml':
            with open(self.config_file, 'w') as f:
                yaml.dump(self.config, f)

    def get(self, key):
        if self.file_type == 'ini':
            return self.config.get(key)
        else:
            keys = key.split('.')
            value = self.config
            for k in keys:
                if k in value:
                    value = value[k]
                else:
                    return None
            return value

    def set(self, key, value):
        if self.file_type == 'ini':
            self.config.set(key, value)
        else:
            self.config[key] = value
            
    def set_all(self, key, value):
        if self.file_type == 'ini':
            self.config[key] = value
        else:
            keys = key.split('.')
            config = self.config
            for k in keys[:-1]:
                if k in config:
                    config = config[k]
                else:
                    config[k] = {}
                    config = config[k]
            config[keys[-1]] = value
    
    def clear(self):
        if self.file_type == 'ini':
            self.config.clear()
        else:
            self.config = None