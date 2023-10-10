import aiohttp
import time
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError
from functools import reduce
from typing import Any
import logging

import yclients_aio_client.constants as c
from yclients_aio_client.base import ApiRequestsStrategy, YclientsGenericModel
from yclients_aio_client.utils.decorators import backoff, debug_log
from yclients_aio_client.utils.validators import validate_method_is_allowed
from yclients_aio_client.exceptions import (
    YclientsServerError,
    YclientsRateLimitted,
    HttpClientError,
    UnparsableResponse,
)

logger = logging.getLogger(__name__)


class AsyncWebClient(ApiRequestsStrategy):
    """HTTP Web client based on aiohttp library.

    Args:
        timeout (int): API requests timeout.
        raise_client_errors (bool): Raise exceptions for responses with 4xx HTTP-code.
        parent (BaseClient): The parent class of the main facade, which is embedded (injected) in the response model
                             to perform manipulations with itself, for example, to delete the received resource.
    """

    def __init__(
        self,
        *,
        timeout: int = 5,
        raise_client_errors: bool = True,
        parent: object | None = None,
    ) -> None:
        self._headers = {}
        self._timeout = timeout
        self._raise_client_errors = raise_client_errors
        self._parent = parent  # hack: shortcut for self object manipulate via injected parent facade
        self._set_base_headers()

    def _set_base_headers(self):
        """Set basic headers required by YCLIENTS."""
        self._headers.update({"Content-Type": "application/json", "Accept": "application/vnd.api.v2+json"})

    def set_auth_headers(self, partner_token: str):  # pylint: disable=W0222
        """Set authorization headers to client."""
        self._headers.update({"Authorization": f"Bearer {partner_token}"})

    def set_custom_global_headers(self, headers: dict = {}) -> None:  # pylint: disable=W0102
        """Set custom provided headers for all requests."""
        if headers:
            self._headers.update(headers)

    def _merge_headers(self, headers: dict):
        """Reduce headers: basic, auth and user provided."""
        return reduce(lambda l, r: {**l, **r}, [self._headers, headers])

    @staticmethod
    def _parse_response(
        parent: object, status: int, response_headers: dict, response: Any, response_data_model: Any
    ) -> YclientsGenericModel | Any:
        """Convert response from YCLIENTS API to provided response model."""
        if response_data_model is None:
            return response

        if not isinstance(response, dict):
            raise UnparsableResponse(
                f"Not JSON response from YCLIENS API. "
                f"Status: {status}, Headers: {response_headers}, "
                f"Response: {response}, Expected model: {response_data_model}, "
                f"Received response type: {type(response)}"
            )

        data = response.get("data", None)
        if isinstance(data, dict):
            parsed_data = response_data_model(**data) if data else None
        elif isinstance(data, list):
            parsed_data = [response_data_model(**dict_) for dict_ in data]
        else:
            logger.warning(f"Strange data from YCLIENTS API: {type(data)}: {data}")
            parsed_data = data

        return YclientsGenericModel(
            parent=parent,
            success=response.get("success"),
            data=parsed_data,
            meta=response.get("meta"),
            status=status,
            response_headers=response_headers,
        )

    @backoff(
        exceptions=(ClientConnectorError, YclientsServerError),
        max_tries=c.backoff_settings.max_tries,
        jitter=c.backoff_settings.jitter,
        base_delay=c.backoff_settings.base_delay,
        expo_factor=c.backoff_settings.expo_factor,
    )
    @debug_log
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
        """Async wrapper for make HTTP requests based on aiohttp."""
        validate_method_is_allowed(method)

        if user_token is not None:
            authorization_headers = self._headers.get("Authorization")
            self._headers["Authorization"] = f"{authorization_headers}, User {user_token}"

        if headers is None:
            headers = self._headers
        else:
            headers = self._merge_headers(headers)
        logger.debug(f"Merged request headers: {headers}")

        async with aiohttp.ClientSession() as session:
            logger.debug(f"Trying make request {method.upper()} {url} params={params}")
            start_time = time.time()
            # fmt: off
            async with session.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                timeout=self._timeout
            ) as response:  # fmt: on
                try:
                    result = await response.json()
                except (json.JSONDecodeError, ContentTypeError):
                    result = await response.text()
                finally:
                    await session.close()
                    elapsed = time.time() - start_time
                    logger.debug(f"Request with ID {response.headers.get('x-request-id')} completed in {elapsed:.3f}s")

        if response.status >= 500:
            raise YclientsServerError(
                f"YCLIENTS Server error. Method: {method.upper()}, URL: {url}, "  # pylint: disable=E1120
                f"Params: {params}, HTTP Code: {str(response.status)}, "
                f"X-Request-ID: {response.headers.get('x-request-id')}"
            )
        elif response.status == 429:
            raise YclientsRateLimitted(
                f"Requests rate limit reached for {method.upper()} {url}, details: {result}"
            )  # pylint: disable=E1120
        elif response.status >= 400 and self._raise_client_errors:
            raise HttpClientError(method, url, params, response, result)

        return __class__._parse_response(
            parent=self._parent,
            status=response.status,
            response=result,
            response_headers=response.headers,
            response_data_model=response_data_model,
        )
