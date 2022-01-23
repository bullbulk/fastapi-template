from typing import Optional, Literal

from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    grant_type: Literal["access", "refresh"]


class AccessTokenPayload(TokenPayload):
    grant_type: Literal["access"]


class RefreshTokenPayload(TokenPayload):
    grant_type: Literal["refresh"]
    fingerprint: Optional[str] = None
