from sqlalchemy.orm import Session

from app import models, schemas
from app.core.auth import get_password_hash, verify_password
from app.crud.base import CRUDBase


class CRUDUser(
    CRUDBase[
        models.User,
        schemas.UserResponse,
        schemas.UserCreate,
        schemas.UserUpdate,
        schemas.UserResponse,
    ],
):
    def get_by_email(self, db: Session, *, email: str) -> models.User | None:
        return db.query(models.User).filter(models.User.email == email).first()

    def create(self, db: Session, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def update(  # type: ignore[override]
        self,
        db: Session,
        *,
        db_obj: models.User,
        obj_in: schemas.UserUpdate,
    ) -> models.User:
        if obj_in.password:
            hashed_password = get_password_hash(obj_in.password)
            db_obj.hashed_password = hashed_password
        return super().update(db, db_obj=db_obj, update_schema=obj_in)

    def authenticate(
        self,
        db: Session,
        *,
        email: str,
        password: str,
    ) -> models.User | None:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(
    models.User,
    response_schema_class=schemas.UserResponse,
    list_response_class=schemas.UsersPagedResponse,
)
