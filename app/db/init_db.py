from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine


# noinspection PyUnusedLocal
def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)
