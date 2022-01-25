from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.refresh_session import RefreshSession
from app.schemas.refresh_session import RefreshSessionCreate, RefreshSessionsUpdate


class CRUDRefreshSession(CRUDBase[RefreshSession, RefreshSessionCreate, RefreshSessionsUpdate]):
    @staticmethod
    def get_by_token(db: Session, *, token: str) -> RefreshSession | None:
        return db.query(RefreshSession).filter(RefreshSession.refresh_token == token).first()

    @staticmethod
    def get_active(
            db: Session,
            *,
            user_id: int,
            fingerprint: str
    ) -> RefreshSession | None:
        return (
            db.query(RefreshSession).filter(
                RefreshSession.user_id == user_id,
                RefreshSession.fingerprint == fingerprint
            ).first()
        )

    def create(self, db: Session, *, obj_in: RefreshSessionCreate) -> RefreshSession:
        # noinspection PyArgumentList
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

    def remove_by_token(self, db: Session, *, token: str) -> RefreshSession | None:
        obj = self.get_by_token(db, token=token)
        return self.remove(db, id=obj.id)


refresh_session = CRUDRefreshSession(RefreshSession)
