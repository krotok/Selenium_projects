import json
import os
from typing import Dict, Any
from utils.logger import LoggerConfig


class Config:
    def __init__(self, environment: str = "dev"):
        self.environment = environment
        self.config_data = self._load_config()
        self._setup_logging()
        #TODO  Remove it before commit
        print(f"DEBUG: Config loaded for {environment}")
        print(f"DEBUG: Config keys: {list(self.config_data.keys())}")

    def _load_config(self) -> Dict[str, Any]:
        config_file = f"config/{self.environment}.json"
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found: {config_file}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in configuration file: {e}")

    def _setup_logging(self):
        """Setup logging based on configuration"""
        log_config = self.get('logging', {})
        log_level = log_config.get('level', 'INFO')
        LoggerConfig.setup_logging(log_level=log_level)

    def get(self, key: str, default: Any = None) -> Any:
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

    @property
    def log_level(self) -> str:
        return self.get('logging', {}).get('level', 'INFO')