"""HTTP API client module with resilience features"""

import json
import random
import time
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .logger import get_logger


class CircuitBreakerOpen(RuntimeError):
    """Raised when the circuit breaker rejects a request"""


class APIClient:
    """HTTP API client for making requests with resilience features"""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None,
        max_retries: int = 2,
        backoff_factor: float = 0.5,
        jitter: float = 0.1,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_reset: int = 30,
    ):
        """Initialize API client

        Args:
            base_url: Base URL for API
            timeout: Request timeout in seconds
            headers: Optional default headers
            max_retries: Number of retry attempts for transient errors
            backoff_factor: Base backoff delay (seconds) used for exponential retry delays
            jitter: Random jitter (seconds) added to backoff delays to prevent thundering herd
            circuit_breaker_threshold: Consecutive failures before opening the circuit breaker
            circuit_breaker_reset: Cooldown period (seconds) before allowing requests after the circuit opens
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.default_headers = headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        self.circuit_breaker_threshold = circuit_breaker_threshold
        self.circuit_breaker_reset = circuit_breaker_reset
        self._failure_count = 0
        self._circuit_open_until = 0.0
        self.logger = get_logger()

    def _circuit_is_open(self) -> bool:
        """Check whether the circuit breaker is currently open"""
        if self._circuit_open_until and time.monotonic() < self._circuit_open_until:
            return True

        if self._circuit_open_until and time.monotonic() >= self._circuit_open_until:
            # Cooldown expired: move to half-open and allow a trial request
            self.logger.info("Circuit breaker cooldown expired; allowing trial request")
            self._circuit_open_until = 0.0
        return False

    def _record_failure(self, error: Exception) -> None:
        """Track failures and open the circuit if necessary"""
        self._failure_count += 1
        self.logger.warning(
            f"API request failed ({error}). Failure streak: {self._failure_count}"
        )

        if self._failure_count >= self.circuit_breaker_threshold:
            self._circuit_open_until = time.monotonic() + self.circuit_breaker_reset
            self._failure_count = 0
            self.logger.warning(
                f"Circuit breaker opened for {self.circuit_breaker_reset}s after "
                f"{self.circuit_breaker_threshold} consecutive failures"
            )

    def _reset_resilience_state(self) -> None:
        """Reset failure counters and circuit state after a successful call"""
        if self._failure_count or self._circuit_open_until:
            self.logger.debug("Resetting API client resilience state")
        self._failure_count = 0
        self._circuit_open_until = 0.0

    def _should_retry(self, error: Exception) -> bool:
        """Determine whether an error is retryable"""
        if isinstance(error, URLError):
            return True
        if isinstance(error, HTTPError) and 500 <= error.code < 600:
            return True
        return False

    def _get_backoff_delay(self, attempt: int) -> float:
        """Compute exponential backoff delay with jitter"""
        base_delay = self.backoff_factor * (2 ** attempt)
        return base_delay + random.uniform(0, self.jitter)

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
            CircuitBreakerOpen: If the circuit breaker is open
        """
        if self._circuit_is_open():
            remaining = max(self._circuit_open_until - time.monotonic(), 0)
            raise CircuitBreakerOpen(
                f"Circuit breaker open. Retry after {remaining:.2f} seconds"
            )

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        # Prepare request data
        request_data = None
        if data:
            request_data = json.dumps(data).encode('utf-8')

        request = Request(url, data=request_data, headers=request_headers, method=method)

        for attempt in range(self.max_retries + 1):
            try:
                self.logger.debug(f"Making {method} request to {url}")
                with urlopen(request, timeout=self.timeout) as response:
                    response_data = response.read().decode('utf-8')
                    self._reset_resilience_state()
                    if response_data:
                        return json.loads(response_data)
                    return {}
            except Exception as error:  # noqa: BLE001 - deliberate broad catch for controlled retries
                if not self._should_retry(error) or attempt == self.max_retries:
                    self._record_failure(error)
                    raise

                self._record_failure(error)
                delay = self._get_backoff_delay(attempt)
                self.logger.warning(
                    f"Retrying {method} {url} in {delay:.2f}s "
                    f"(attempt {attempt + 1}/{self.max_retries})"
                )
                time.sleep(delay)

        # Should never reach here because loop either returns or raises
        raise RuntimeError("Unexpected exit from request loop")

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

    def get_resilience_state(self) -> Dict[str, Any]:
        """Expose circuit breaker and retry state for observability"""
        return {
            'failure_streak': self._failure_count,
            'circuit_open_until': self._circuit_open_until,
            'circuit_open': self._circuit_is_open(),
            'max_retries': self.max_retries,
        }
