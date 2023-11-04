import logging

from pydantic import BaseModel
from yclients_aio_client.base import YclientsGenericModel, BaseResponseDataModel

logger = logging.getLogger(__name__)


class YclientsBaseAuth(BaseResponseDataModel):
    id: int
    user_token: str
    phone: str
    login: str
    name: str | None = None
    email: str | None = None
    avatar: str | None = None


class YclientsPartnerAuth(YclientsBaseAuth):
    is_approved: bool


class YclientsAuthResponse(YclientsGenericModel):
    data: YclientsBaseAuth


class YclientsPartnerAuthResponse(YclientsGenericModel):
    data: YclientsPartnerAuth
