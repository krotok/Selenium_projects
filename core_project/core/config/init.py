import json
import os
from typing import Dict, Any
from core_project.core.utils.logger import LoggerConfig


class Config:
    """Base configuration class for all projects"""

    def __init__(self, environment: str = "dev", config_path: str = "config"):
        self.environment = environment
        self.config_path = config_path
        self.config_data = self._load_config()
        self._setup_logging()

    def _load_config(self) -> Dict[str, Any]:
        config_file = f"{self.config_path}/{self.environment}.json"
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
    def browser(self):
        return self.get('browser', 'chrome')

    @property
    def headless(self):
        return self.get('headless', False)

    @property
    def timeout(self):
        return self.get('timeout', 15)