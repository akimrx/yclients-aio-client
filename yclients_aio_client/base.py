from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Any


class ApiRequestsStrategy(ABC):
    @abstractmethod
    def set_auth_headers(self, partner_token: str | None = None):
        """Method for set auth headers to HTTP Client."""

    @abstractmethod
    def set_custom_global_headers(self, headers: dict) -> None:
        """Set custom provided headers for all requests."""

    @abstractmethod
    async def request(
        self,
        method: str,
        url: str,
        *,
        user_token: str | None = None,
        params: dict = None,
        data: Any = None,
        json: dict | None = None,
        headers: dict | None = None,
        response_data_model: Any = None,
    ) -> Any:
        """Method for make API requests."""


class BaseClient:
    """Generic YCLIENTS API Client."""

    def __init__(
        self,
        api_client: ApiRequestsStrategy,
        partner_token: str | None = None,
        main_company_id: str | None = None,
        timeout: int = 5,
        raise_client_erros: bool = True,
    ) -> None:
        self._api_client = api_client
        self._partner_token = partner_token
        self._main_company_id = main_company_id


class YclientsGenericModel(BaseModel):
    """Generic model for YCLIENTS API responses."""

    success: bool
    data: Any
    meta: Any
    status: int
    response_headers: dict = {}
    parent: Any = Field(
        ..., repr=False, exclude=True, init=False
    )  # hack: shortcut for self object manipulate via injected parent facade
