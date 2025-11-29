import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../core'))

from core_project.core.config.init import Config as CoreConfig


class Config(CoreConfig):
    """Herokuapp specific configuration extending core config"""

    def __init__(self, environment: str = "dev"):
        super().__init__(environment, config_path="herokuapp/config")

    @property
    def api_url(self):
        """API URL for Herokuapp"""
        return self.get('api_url', self.base_url)  # Fallback to base_url if api_url not defined

    @property
    def test_users(self):
        """Herokuapp specific test users for various scenarios"""
        return {
            "valid": {
                "username": "tomsmith",
                "password": "SuperSecretPassword!"
            },
            "invalid": {
                "username": "invalid_user",
                "password": "wrong_password"
            },
            "empty": {
                "username": "",
                "password": ""
            },
            "sql_injection": {
                "username": "admin' OR '1'='1",
                "password": "password"
            }
        }