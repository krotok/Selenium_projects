import requests
from typing import Dict, Any, Optional
from utils.log_decorators import LoggingMixin, log_function_call, log_api_call


class WireMockService(LoggingMixin):
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger.debug(f"Initialized WireMockService with base URL: {base_url}")

    @log_api_call("Create stub mapping")
    @log_function_call(log_args=True, log_result=True)
    def create_stub(self, stub_config: Dict[str, Any]) -> bool:
        """Create a new stub mapping"""
        url = f"{self.base_url}/__admin/mappings"
        response = self.session.post(url, json=stub_config)

        if response.status_code == 201:
            self.logger.info(f"Stub created successfully: {stub_config['request']['url']}")
            return True
        else:
            self.logger.error(f"Failed to create stub: {response.text}")
            return False

    @log_api_call("Create login stub")
    @log_function_call(log_args=True, log_result=True)
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
        self.logger.info(f"Creating login stub for user: {username} (success: {success})")
        return self.create_stub(stub_config)

    @log_api_call("Create dynamic content stub")
    @log_function_call(log_args=True, log_result=True)
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
        self.logger.info(f"Creating dynamic content stub with delay: {delay}s")
        return self.create_stub(stub_config)

    @log_api_call("Reset mappings")
    @log_function_call(log_result=True)
    def reset_mappings(self) -> bool:
        """Reset all stub mappings"""
        url = f"{self.base_url}/__admin/mappings/reset"
        response = self.session.post(url)
        success = response.status_code == 200
        if success:
            self.logger.info("WireMock mappings reset successfully")
        else:
            self.logger.warning("Failed to reset WireMock mappings")
        return success

    @log_api_call("Get received requests")
    @log_function_call(log_result=True)
    def get_requests(self) -> Dict[str, Any]:
        """Get all received requests"""
        url = f"{self.base_url}/__admin/requests"
        response = self.session.get(url)
        return response.json()