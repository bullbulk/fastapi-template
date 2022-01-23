from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


# Shared properties
class RefreshSessionBase(BaseModel):
    user_id: Optional[int] = None
    refresh_token: Optional[str] = None
    expires_delta: Optional[timedelta] = None


# Properties to validate on session creation
class RefreshSessionCreate(RefreshSessionBase):
    fingerprint: Optional[str] = None


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
    refresh_token: Optional[str] = None
