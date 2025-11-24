import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ApiService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HeroKuapp-Test-Automation/1.0'
        })

    def get_status(self) -> Dict[str, Any]:
        """Get application status"""
        response = self.session.get(f"{self.base_url}/status")
        response.raise_for_status()
        return response.json()

    def get_all_elements(self) -> Dict[str, Any]:
        """Get all challenge elements"""
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return {"status_code": response.status_code, "content": response.text}

    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate via API (if available)"""
        # This is a mock implementation since Herokuapp doesn't have auth API
        # In real scenario, this would call actual auth endpoint
        logger.info(f"Mock authentication for user: {username}")
        return {
            "authenticated": True,
            "user": username,
            "token": "mock_jwt_token"
        }

    def close(self):
        """Close session"""
        self.session.close()
        