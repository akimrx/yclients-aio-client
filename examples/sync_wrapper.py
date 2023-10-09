import asyncio
import logging
from typing import Coroutine, Any
from yclients_aio_client import AsyncYclientsClient


logging.basicConfig(
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)
partner_token = "xxxxxxxxxxxxxxxxxxxx"
yclients = AsyncYclientsClient(partner_token=partner_token, raise_client_errors=True)


def _(coroutine: Coroutine) -> Any:
    """Wrapper for run async fucntion synchronous."""
    return asyncio.run(coroutine)


def authenticate_user(user: str, password: str) -> str:
    """Get user token by user:password pair."""
    result = _(yclients.auth.get_user_token(user, password))
    return result.data.user_token


def main() -> None:
    user = "user@example.com"
    password = "user_password"
    print("User token:", authenticate_user(user, password))


if __name__ == "__main__":
    main()
