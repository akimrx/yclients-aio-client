import logging

from pydantic import BaseModel
from yclients_aio_client.base import YclientsGenericModel

logger = logging.getLogger(__name__)


class YclientsBaseAuth(BaseModel):
    id: int
    user_token: str
    phone: str
    login: str
    name: str | None = None
    email: str | None = None
    avatar: str | None = None

    class Config:
        extra = "ignore"

    def __init__(self, **data):
        extra_fields = set(data.keys()) - set(self.__fields__)
        if extra_fields:
            unspecified = ", ".join(extra_fields)
            logger.warning(
                f"Found fields that are not documented in the API specification. "
                f"The following fields will be ignored: {unspecified}"
            )
        super().__init__(**data)


class YclientsPartnerAuth(YclientsBaseAuth):
    is_approved: bool


class YclientsAuthResponse(YclientsGenericModel):
    data: YclientsBaseAuth


class YclientsPartnerAuthResponse(YclientsGenericModel):
    data: YclientsPartnerAuth
