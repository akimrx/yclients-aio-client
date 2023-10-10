from conftest import (
    fake_response_post_auth,
    fake_response_post_booking_auth,
)
from yclients_aio_client import AsyncYclientsClient
from yclients_aio_client.base import YclientsGenericModel
from yclients_aio_client.yclients.auth.models import YclientsPartnerAuth, YclientsBaseAuth


async def test_create_user_token(client: AsyncYclientsClient) -> None:
    response = await client.auth.get_user_token("fake_login", "fake_password")
    assert isinstance(response, YclientsGenericModel)
    assert isinstance(response.data, YclientsPartnerAuth)
    assert isinstance(response.parent, AsyncYclientsClient)
    assert response.response_headers.get("X-Request-ID") == "mock-request-id"
    assert response.status == 200
    assert response.data.model_dump() == fake_response_post_auth["data"]


async def test_create_booking_token_by_password(client: AsyncYclientsClient) -> None:
    response = await client.auth.get_client_token_by_password("fake_login", "fake_password")
    assert isinstance(response, YclientsGenericModel)
    assert isinstance(response.data, YclientsBaseAuth)
    assert isinstance(response.parent, AsyncYclientsClient)
    assert response.response_headers.get("X-Request-ID") == "mock-request-id"
    assert response.status == 200
    assert response.data.model_dump() == fake_response_post_booking_auth["data"]


async def test_create_booking_token_by_sms(client: AsyncYclientsClient) -> None:
    response = await client.auth.get_client_token_by_sms_code("79991234567", "1234")
    assert isinstance(response, YclientsGenericModel)
    assert isinstance(response.data, YclientsBaseAuth)
    assert isinstance(response.parent, AsyncYclientsClient)
    assert response.response_headers.get("X-Request-ID") == "mock-request-id"
    assert response.status == 200
    assert response.data.model_dump() == fake_response_post_booking_auth["data"]
