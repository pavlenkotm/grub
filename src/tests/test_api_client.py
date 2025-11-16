"""Tests for the resilient API client"""

import time
import unittest
from urllib.error import URLError
from unittest.mock import patch

from src.utils.api_client import APIClient, CircuitBreakerOpen


class _FakeResponse:
    """Lightweight response stub for urlopen context manager"""

    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class APIClientResilienceTests(unittest.TestCase):
    @patch('src.utils.api_client.time.sleep')
    @patch('src.utils.api_client.urlopen')
    def test_retry_recovers_after_transient_error(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = [URLError('temporary'), _FakeResponse(b'{"status": "ok"}')]
        client = APIClient('https://example.com', max_retries=2, backoff_factor=0.0, jitter=0.0)

        result = client.get('/ping')

        self.assertEqual(result['status'], 'ok')
        self.assertEqual(mock_urlopen.call_count, 2)
        state = client.get_resilience_state()
        self.assertFalse(state['circuit_open'])
        self.assertEqual(state['failure_streak'], 0)

    @patch('src.utils.api_client.time.sleep')
    @patch('src.utils.api_client.urlopen')
    def test_circuit_breaker_opens_after_repeated_failures(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = URLError('down')
        client = APIClient(
            'https://example.com',
            max_retries=0,
            circuit_breaker_threshold=2,
            circuit_breaker_reset=60,
        )

        with self.assertRaises(URLError):
            client.get('/fail')
        with self.assertRaises(URLError):
            client.get('/fail')

        self.assertEqual(mock_urlopen.call_count, 2)
        state = client.get_resilience_state()
        self.assertTrue(state['circuit_open'])

        with self.assertRaises(CircuitBreakerOpen):
            client.get('/fail')
        self.assertEqual(mock_urlopen.call_count, 2)

    @patch('src.utils.api_client.time.sleep')
    def test_circuit_breaker_recovers_after_cooldown(self, mock_sleep):
        client = APIClient(
            'https://example.com',
            max_retries=0,
            circuit_breaker_threshold=1,
            circuit_breaker_reset=1,
        )

        with patch('src.utils.api_client.urlopen', side_effect=URLError('boom')):
            with self.assertRaises(URLError):
                client.get('/fail')

        self.assertTrue(client.get_resilience_state()['circuit_open'])

        client._circuit_open_until = time.monotonic() - 0.5
        with patch('src.utils.api_client.urlopen', return_value=_FakeResponse(b'{}')):
            result = client.get('/recovered')

        self.assertEqual(result, {})
        self.assertFalse(client.get_resilience_state()['circuit_open'])


if __name__ == '__main__':
    unittest.main()
