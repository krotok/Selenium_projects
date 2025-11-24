import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class WireMockService:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()

    def create_stub(self, stub_config: Dict[str, Any]) -> bool:
        """Create a new stub mapping"""
        url = f"{self.base_url}/__admin/mappings"
        response = self.session.post(url, json=stub_config)

        if response.status_code == 201:
            logger.info(f"Stub created successfully: {stub_config['request']['url']}")
            return True
        else:
            logger.error(f"Failed to create stub: {response.text}")
            return False

    def create_login_stub(self, username: str, success: bool = True) -> bool:
        """Create stub for login endpoint"""
        stub_config = {
            "request": {
                "method": "POST",
                "url": "/api/login",
                "bodyPatterns": [
                    {
                        "contains": username
                    }
                ]
            },
            "response": {
                "status": 200 if success else 401,
                "jsonBody": {
                    "authenticated": success,
                    "user": username if success else None,
                    "message": "Login successful" if success else "Invalid credentials"
                },
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        }
        return self.create_stub(stub_config)

    def create_dynamic_content_stub(self, delay: int = 0) -> bool:
        """Create stub for dynamic content with delay"""
        stub_config = {
            "request": {
                "method": "GET",
                "url": "/api/dynamic-content"
            },
            "response": {
                "status": 200,
                "jsonBody": {
                    "content": "Hello World!",
                    "loaded": True
                },
                "fixedDelayMilliseconds": delay * 1000
            }
        }
        return self.create_stub(stub_config)

    def reset_mappings(self) -> bool:
        """Reset all stub mappings"""
        url = f"{self.base_url}/__admin/mappings/reset"
        response = self.session.post(url)
        return response.status_code == 200

    def get_requests(self) -> Dict[str, Any]:
        """Get all received requests"""
        url = f"{self.base_url}/__admin/requests"
        response = self.session.get(url)
        return response.json()