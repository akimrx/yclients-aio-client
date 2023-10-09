from typing import Any

import yclients_aio_client.constants as c
import yclients_aio_client.test.fake_auth as fake_auth
from yclients_aio_client.base import ApiRequestsStrategy, YclientsGenericModel
from yclients_aio_client.utils.request import AsyncWebClient


class MockWebClient(ApiRequestsStrategy):
    """Mock HTTP Client for testing."""

    def __init__(
        self,
        *,
        timeout: int = 5,
        raise_client_errors: bool = True,
        parent: object | None = None,
    ) -> None:
        self._raise_client_errors = raise_client_errors
        self._parent = parent

    def set_auth_headers(self, partner_token: str):
        pass

    def set_custom_global_headers(self, headers: dict = {}) -> None:
        pass

    @staticmethod
    def _parse_response(
        parent: object,
        status: int,
        response_headers: dict,
        response: Any,
        response_data_model: Any
    ) -> Any:
        return AsyncWebClient._parse_response(
            parent,
            status,
            response_headers,
            response,
            response_data_model
        )

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
        response_data_model: Any = None
    ) -> YclientsGenericModel | dict | Any:
        """Make request to Fake YCLIENTS API."""
        match (method, url):
            case ("post", "https://api.yclients.com/api/v1/auth"):
                response = fake_auth.post_staff_user_auth_response
            case ("post", "https://api.yclients.com/api/v1/booking/auth"):
                response = fake_auth.post_booking_user_auth_response
            case ("post", "https://api.yclients.com/api/v1/user/auth"):
                response = fake_auth.post_booking_user_auth_response
            case _:
                return

        return __class__._parse_response(
            self._parent,
            status=200,
            response_headers={"X-Request-ID": "mock-request-id"},
            response=response,
            response_data_model=response_data_model
        )
