import requests
from typing import Dict, Any, Optional
from utils.log_decorators import LoggingMixin, log_api_call, log_function_call


class ApiService(LoggingMixin):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HeroKuapp-Test-Automation/1.0'
        })
        self.logger.debug(f"Initialized ApiService with base URL: {base_url}")

    @log_api_call("Get application status")
    @log_function_call(log_result=True)
    def get_status(self) -> Dict[str, Any]:
        """Get application status"""
        response = self.session.get(f"{self.base_url}/status")
        response.raise_for_status()
        return response.json()

    @log_api_call("Get all challenge elements")
    @log_function_call(log_result=True)
    def get_all_elements(self) -> Dict[str, Any]:
        """Get all challenge elements"""
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return {"status_code": response.status_code, "content": response.text}

    @log_api_call("Authenticate user")
    @log_function_call(log_args=True, log_result=True)
    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate via API (if available)"""
        self.logger.info(f"Mock authentication for user: {username}")
        return {
            "authenticated": True,
            "user": username,
            "token": "mock_jwt_token"
        }

    def close(self):
        """Close session"""
        self.session.close()
        self.logger.debug("ApiService session closed")