from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.refresh_session import RefreshSession
from app.schemas.refresh_session import RefreshSessionCreate, RefreshSessionsUpdate


class CRUDRefreshSession(CRUDBase[RefreshSession, RefreshSessionCreate, RefreshSessionsUpdate]):
    def get_by_token(self, db: Session, *, token: str) -> Optional[RefreshSession]:
        return db.query(RefreshSession).filter(RefreshSession.refresh_token == token).first()

    def get_active(
            self,
            db: Session,
            *,
            user_id: int,
            fingerprint: str
    ) -> Optional[RefreshSession]:
        return (
            db.query(RefreshSession).filter(
                RefreshSession.user_id == user_id,
                RefreshSession.fingerprint == fingerprint
            ).first()

        )

    def create(self, db: Session, *, obj_in: RefreshSessionCreate) -> RefreshSession:
        db_obj = RefreshSession(
            user_id=obj_in.user_id,
            refresh_token=obj_in.refresh_token,
            fingerprint=obj_in.fingerprint,
            expires_in=datetime.utcnow() + obj_in.expires_delta,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_by_token(self, db: Session, *, token: str) -> Optional[RefreshSession]:
        obj = self.get_by_token(db, token=token)
        return self.remove(db, id=obj.id)


refresh_session = CRUDRefreshSession(RefreshSession)
