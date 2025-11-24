import json
import os


class Config:
    def __init__(self, environment="dev"):
        self.environment = environment
        self.config_data = self._load_config()

    def _load_config(self):
        config_file = f"config/{self.environment}.json"
        with open(config_file, 'r') as file:
            return json.load(file)

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    @property
    def base_url(self):
        return self.get('base_url')

    @property
    def api_url(self):
        return self.get('api_url')

    @property
    def db_config(self):
        return {
            'host': self.get('db_host'),
            'port': self.get('db_port'),
            'database': self.get('db_name'),
            'user': self.get('db_user'),
            'password': self.get('db_password')
        }