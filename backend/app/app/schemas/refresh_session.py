from datetime import timedelta

from pydantic import BaseModel


# Shared properties
class RefreshSessionBase(BaseModel):
    user_id: int | None = None
    refresh_token: str | None = None
    expires_delta: timedelta | None = None


# Properties to validate on session creation
class RefreshSessionCreate(RefreshSessionBase):
    fingerprint: str | None = None


class RefreshSessionsUpdate(RefreshSessionBase):
    pass


# Properties shared by models stored in DB
class RefreshSessionInDBBase(RefreshSessionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties stored in DB
class RefreshSessionInDB(RefreshSessionInDBBase):
    refresh_token: str | None = None
