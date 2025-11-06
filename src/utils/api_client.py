"""
HTTP API client module
"""

import json
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from .logger import get_logger


class APIClient:
    """HTTP API client for making requests"""

    def __init__(self, base_url: str, timeout: int = 30, headers: Optional[Dict[str, str]] = None):
        """Initialize API client

        Args:
            base_url: Base URL for API
            timeout: Request timeout in seconds
            headers: Optional default headers
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.default_headers = headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.logger = get_logger()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Optional request data
            headers: Optional request headers

        Returns:
            Response data as dictionary

        Raises:
            HTTPError: On HTTP error
            URLError: On URL/network error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        # Prepare request data
        request_data = None
        if data:
            request_data = json.dumps(data).encode('utf-8')

        request = Request(url, data=request_data, headers=request_headers, method=method)

        try:
            self.logger.debug(f"Making {method} request to {url}")
            with urlopen(request, timeout=self.timeout) as response:
                response_data = response.read().decode('utf-8')
                if response_data:
                    return json.loads(response_data)
                return {}
        except HTTPError as e:
            self.logger.error(f"HTTP Error {e.code}: {e.reason}")
            raise
        except URLError as e:
            self.logger.error(f"URL Error: {e.reason}")
            raise
        except Exception as e:
            self.logger.error(f"Request failed: {e}")
            raise

    def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make GET request

        Args:
            endpoint: API endpoint
            headers: Optional request headers

        Returns:
            Response data
        """
        return self._make_request('GET', endpoint, headers=headers)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make POST request

        Args:
            endpoint: API endpoint
            data: Request data
            headers: Optional request headers

        Returns:
            Response data
        """
        return self._make_request('POST', endpoint, data=data, headers=headers)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make PUT request

        Args:
            endpoint: API endpoint
            data: Request data
            headers: Optional request headers

        Returns:
            Response data
        """
        return self._make_request('PUT', endpoint, data=data, headers=headers)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make DELETE request

        Args:
            endpoint: API endpoint
            headers: Optional request headers

        Returns:
            Response data
        """
        return self._make_request('DELETE', endpoint, headers=headers)

    def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
        """Set authentication token in default headers

        Args:
            token: Authentication token
            token_type: Token type (Bearer, Token, etc.)
        """
        self.default_headers['Authorization'] = f"{token_type} {token}"
        self.logger.info("Authentication token set")
