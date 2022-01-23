from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class RefreshSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    refresh_token = Column(String, unique=True, index=True, nullable=False)
    fingerprint = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_in = Column(DateTime, nullable=False,
                        default=datetime.utcnow)  # expires in the moment of creation by default
    user = relationship("User")
