import yclients_aio_client.constants as c

from yclients_aio_client.utils.validators import validate_company_id
from yclients_aio_client.base import (
    BaseClient,
    BaseInjectedClient,
    YclientsGenericModel,
    ApiRequestsStrategy,
)
from yclients_aio_client.yclients.auth.models import (
    YclientsBaseAuth,
    YclientsAuthResponse,
    YclientsPartnerAuth,
    YclientsPartnerAuthResponse,
)

# TODO (akimrx): use pydantic models `FooPayload` instead `data`: dict ??


class YclientsAuthClient(BaseInjectedClient):
    """Web client for authentication in the YCLIENTS API."""

    def __init__(self, parent: BaseClient):
        self._parent = parent

    @property
    def _api(self) -> ApiRequestsStrategy:
        """Alias for API adapter."""
        return self._parent._api_client

    # TODO: caching + invalidation
    async def get_user_token(self, login: str, password: str, **kwargs) -> YclientsPartnerAuthResponse:
        """Authenticate staff (employee) YCLIENTS user.

        Auth required:
            * Partner token

        URI Path: `/auth`
        """
        url = f"{c.YCLIENTS_API_URL}/auth"
        data = {"login": login, "password": password}
        return await self._api.request("post", url, json=data, response_data_model=YclientsPartnerAuth, **kwargs)

    async def get_client_token_by_password(self, login: str, password: str, **kwargs) -> YclientsAuthResponse:
        """Authenticate booking user via user:password pair.

        Auth required:
            * Partner token

        URI Path: `/booking/auth`
        """
        url = f"{c.YCLIENTS_API_URL}/booking/auth"
        data = {"login": login, "password": password}
        return await self._api.request("post", url, json=data, response_data_model=YclientsBaseAuth, **kwargs)

    async def generate_sms_code(
        self, phone: str, fullname: str, company_id: str | None = None, **kwargs
    ) -> YclientsGenericModel:
        """Generate SMS-code for authenticate booking user.

        Auth required:
            * Partner token

        URI Path: `/book_code/{company_id}`
        """
        company = validate_company_id(self._parent._main_company_id, company_id)
        url = f"{c.YCLIENTS_API_URL}/book_code/{company}"
        data = {"phone": phone, "fullname": fullname}
        return await self._api.request("post", url, json=data, **kwargs)

    async def get_client_token_by_sms_code(self, phone: str, code: str, **kwargs) -> YclientsAuthResponse:
        """Authenticate booking user via SMS-code.

        Auth required:
            * Partner token

        URI Path: `/user/auth`
        """
        url = f"{c.YCLIENTS_API_URL}/user/auth"
        data = {"phone": phone, "code": code}
        return await self._api.request("post", url, json=data, response_data_model=YclientsBaseAuth, **kwargs)
