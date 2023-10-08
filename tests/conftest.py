import asyncio
import pytest

from yclients_aio_client import AsyncYclientsClient
from yclients_aio_client.test.client import MockWebClient


@pytest.fixture(scope="session")
async def client() -> MockWebClient:
    """Returns Mock YCLIENTS client for testing."""
    return AsyncYclientsClient(
        partner_token="fake_token",
        api_client=MockWebClient
    )


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
