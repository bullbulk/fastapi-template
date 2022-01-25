from typing import Literal

from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: int | None = None
    grant_type: Literal["access", "refresh"]


class AccessTokenPayload(TokenPayload):
    grant_type: Literal["access"]


class RefreshTokenPayload(TokenPayload):
    grant_type: Literal["refresh"]
    fingerprint: str | None = None
