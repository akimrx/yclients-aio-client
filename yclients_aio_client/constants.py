from functools import lru_cache
from pydantic_settings import BaseSettings

YCLIENTS_BASE_URL = "https://api.yclients.com"
YCLIENTS_API_URL = f"{YCLIENTS_BASE_URL}/api/v1"

ALLOWED_HTTP_METHODS = (
    "get",
    "post",
    "put",
    "patch",
    "delete",
)


class YclientsClientBackoffSettings(BaseSettings):
    """Backoff settings for AsyncApiAdapter.

    Supports environment variables:
        * YCLIENTS_BACKOFF_MAX_TRIES=:type int:
        * YCLIENTS_BACKOFF_JITTER=:type bool:
        * YCLIENTS_BACKOFF_BASE_DELAY=:type int, type float:
        * YCLIENTS_BACKOFF_EXPO_FACTOR=:type int, type float:
    """

    max_tries: int = 3
    jitter: bool = True
    base_delay: int | float = 0.5
    expo_factor: int | float = 2.1

    class Config:
        env_prefix = "YCLIENTS_BACKOFF_"
        case_sensitive = False
        env_nested_delimiter = "__"
        env_file = ".env"


@lru_cache
def _get_backoff_settings():
    return YclientsClientBackoffSettings()


backoff_settings = _get_backoff_settings()
