import asyncio
import pytest
from typing import Any

import yclients_aio_client.constants as c
from yclients_aio_client.base import ApiRequestsStrategy, YclientsGenericModel
from yclients_aio_client.utils.request import AsyncWebClient
from yclients_aio_client import AsyncYclientsClient


fake_response_post_auth = {
    "success": True,
    "data": {
        "id": 123456,
        "user_token": "wec23fh8cDfFV4432fc352456",
        "name": "Samson Gudini",
        "phone": "79161001010",
        "login": "79161001010",
        "email": "test@test.com",
        "avatar": "https://assets.yclients.com/general/0/01/123456789098765_12345678909876.png",
        "is_approved": True,
    },
    "meta": {},
}

fake_response_post_booking_auth = {
    "success": True,
    "data": {
        "id": 123456,
        "user_token": "wec23fh8cDfFV4432fc352456",
        "name": "Ariel Lindberg",
        "phone": "79161001010",
        "login": "79161001010",
        "email": "test@test.com",
        "avatar": "https://assets.yclients.com/general/0/01/123456789098765_12345678909876.png",
    },
    "meta": {},
}


class MockWebClient(ApiRequestsStrategy):
    """Mock HTTP Client for testing."""

    def __init__(self, *, timeout: int = 5, raise_client_errors: bool = True, parent: object | None = None) -> None:
        self._raise_client_errors = raise_client_errors
        self._parent = parent

    def set_auth_headers(self, partner_token: str):
        pass

    def set_custom_global_headers(self, headers: dict = {}) -> None:
        pass

    @staticmethod
    def _parse_response(
        parent: object, status: int, response_headers: dict, response: Any, response_data_model: Any
    ) -> Any:
        return AsyncWebClient._parse_response(parent, status, response_headers, response, response_data_model)

    async def request(
        self,
        method: str,
        url: str,
        *,
        user_token: str = None,
        params: dict = None,
        data: Any = None,
        json: dict | None = None,
        headers: dict | None = None,
        response_data_model: Any = None,
    ) -> YclientsGenericModel | dict | Any:
        """Make request to Fake YCLIENTS API."""
        match (method, url):
            case ("post", "https://api.yclients.com/api/v1/auth"):
                response = fake_response_post_auth
            case ("post", "https://api.yclients.com/api/v1/booking/auth"):
                response = fake_response_post_booking_auth
            case ("post", "https://api.yclients.com/api/v1/user/auth"):
                response = fake_response_post_booking_auth
            case _:
                return

        return __class__._parse_response(
            self._parent,
            status=200,
            response_headers={"X-Request-ID": "mock-request-id"},
            response=response,
            response_data_model=response_data_model,
        )


@pytest.fixture(scope="session")
async def client() -> MockWebClient:
    """Returns Mock YCLIENTS client for testing."""
    return AsyncYclientsClient(partner_token="fake_token", api_client=MockWebClient)


@pytest.fixture(scope="session")
def event_loop(request):
    """Event loop for test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
