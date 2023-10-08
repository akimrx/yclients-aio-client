import aiohttp
import time
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError
from functools import reduce
from typing import Any
import logging

import yclients_aio_client.constants as c
from yclients_aio_client.base import ApiRequestsStrategy, YclientsGenericModel
from yclients_aio_client.utils.decorators import backoff, debug_log
from yclients_aio_client.exceptions import (
    YclientsServerError,
    YclientsRateLimitted,
    HttpClientError,
    MethodNotAllowed,
    UnparsableResponse,
)

logger = logging.getLogger(__name__)


class AsyncWebClient(ApiRequestsStrategy):
    """HTTP Web client based on aiohttp library."""

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
        self._headers.update({
            "Content-Type": "application/json",
            "Accept": "application/vnd.api.v2+json"
        })

    def set_auth_headers(self, partner_token: str):
        """Set authorization headers to client."""
        self._headers.update({"Authorization": f"Bearer {partner_token}"})

    def set_custom_global_headers(self, headers: dict = {}) -> None:
        """Set custom provided headers for all requests."""
        if headers:
            self._headers.update(headers)

    def _merge_headers(self, headers: dict):
        """Reduce headers: basic, auth and user provided."""
        return reduce(lambda l, r: {**l, **r}, [self._headers, headers])

    @staticmethod
    def _parse_response(parent: object, status: int, response_headers: dict, response: Any, response_data_model: Any):
        """Convert response from YCLIENTS API to provided response model."""
        if not isinstance(response, dict):  # TODO: list?
            raise UnparsableResponse(
                f"Not JSON response from YCLIENS API. "
                f"Status: {status}, Headers: {response_headers}, "
                f"Response: {response}, Expected model: {response_data_model}"
            )

        if response_data_model is not None:
            data = response.get("data", None)
            return YclientsGenericModel(
                parent=parent,
                success=response.get("success"),
                data=response_data_model(**data) if isinstance(data, dict) else data,  # TODO: lists support
                meta=response.get("meta"),
                status=status,
                response_headers=response_headers
            )
        return response

    @backoff(
        exceptions=(ClientConnectorError, YclientsServerError),  # FIXME: remove HttpClientError before release, just for test
        max_tries=c.backoff_settings.max_tries,
        jitter=c.backoff_settings.jitter,
        base_delay=c.backoff_settings.base_delay,
        expo_factor=c.backoff_settings.expo_factor
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
        response_data_model: Any = None
    ) -> YclientsGenericModel | dict | Any:
        """Async wrapper for make HTTP requests based on aiohttp."""

        if not isinstance(method, str) or method.lower() not in c.ALLOWED_HTTP_METHODS:
            raise MethodNotAllowed(
                f"Bad HTTP method received. "
                f"Allowed methods: {c.ALLOWED_HTTP_METHODS}"
            )

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
            async with session.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                timeout=self._timeout
            ) as response:
                try:
                    result = await response.json()
                except (json.JSONDecodeError, ContentTypeError):
                    result = await response.text()
                finally:
                    await session.close()
                    elapsed = time.time() - start_time
                    logger.debug(
                        f"Request with ID {response.headers.get('x-request-id')} "
                        f"completed in {elapsed:.3f}s"
                    )

        if response.status >= 500:
            raise YclientsServerError(
                f"YCLIENTS Server error. Method: {method.upper()}, URL: {url}, "
                f"Params: {params}, HTTP Code: {str(response.status)}, "
                f"X-Request-ID: {response.headers.get('x-request-id')}"
            )
        elif response.status == 429:
            raise YclientsRateLimitted(f"Requests rate limit reached for {method.upper()} {url}, details: {result}")
        elif response.status >= 400 and self._raise_client_errors:
            raise HttpClientError(method, url, params, response, result)

        return __class__._parse_response(
            parent=self._parent,
            status=response.status,
            response=result,
            response_headers=response.headers,
            response_data_model=response_data_model
        )