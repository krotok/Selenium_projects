import requests
import logging
from typing import Dict, Any, Optional
from core_project.core.utils.log_decorators import LoggingMixin, log_function_call
import requests
import logging
from typing import Dict, Any, Optional


class ApiService(LoggingMixin):
    """Generic API service for REST API testing"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Test-Automation-Framework/1.0'
        })
        self.logger.debug(f"Initialized ApiService with base URL: {base_url}")

    @log_function_call(log_args=True, log_result=True)
    def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Perform GET request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    @log_function_call(log_args=True, log_result=True)
    def post(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Perform POST request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    @log_function_call(log_args=True, log_result=True)
    def put(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Perform PUT request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json()

    @log_function_call(log_args=True, log_result=True)
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Perform DELETE request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url)
        response.raise_for_status()
        return {"status": "success"}

    @log_function_call(log_args=True, log_result=True)
    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Mock authentication method - in real scenario would call actual auth endpoint"""
        self.logger.info(f"Mock authentication for user: {username}")
        # This is a mock implementation since Herokuapp doesn't have real auth API
        return {
            "authenticated": True,
            "user": username,
            "token": f"mock_jwt_token_{username}",
            "expires_in": 3600
        }

    def close(self):
        """Close session"""
        self.session.close()
        self.logger.debug("ApiService session closed")