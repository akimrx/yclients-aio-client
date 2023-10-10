import logging

from yclients_aio_client.base import ApiRequestsStrategy, BaseClient
from yclients_aio_client.utils.request import AsyncWebClient
from yclients_aio_client.yclients.auth.client import YclientsAuthClient

logger = logging.getLogger(__name__)


class AsyncYclientsClient(BaseClient):
    """Asynchronous client for YCLIENTS API.

    Args:
        partner_token (str): Bearer token.
        main_company_id (str): Default YCLIENTS company ID.
        timeout (int): API requests timeout.
        api_client (ApiRequestsStrategy): Strategy for make API requests, i.e. API Client.
        raise_client_errors (bool): Raise exceptions for responses with 4xx HTTP-code.

    Methods:
        set_custom_global_headers (dict): Allows you to set the headers that will be used in each API request.

    Injected clients (provided as property):
        auth (YclientsAuthClient): Client for YCLIENTS authentication.
    """

    def __init__(
        self,
        *,
        partner_token: str,
        main_company_id: str | None = None,
        timeout: int = 5,
        api_client: ApiRequestsStrategy = AsyncWebClient,
        raise_client_errors: bool = True
    ) -> None:
        self._partner_token = partner_token
        self._main_company_id = main_company_id
        self._api_client = api_client(
            timeout=timeout,
            raise_client_errors=raise_client_errors,
            parent=self  # hack: shortcut for self object manipulate via injected parent facade
        )
        self._api_client.set_auth_headers(partner_token=self._partner_token)

    def set_custom_global_headers(self, headers: dict):
        """Shortcut for set global headers to API adapter."""
        return self._api_client.set_custom_global_headers(headers)

    @property
    def auth(self) -> YclientsAuthClient:
        """Provides an interface for authentication in the YCLIENTS API."""
        return YclientsAuthClient(self)


__all__ = [
    "AsyncYclientsClient",
]
