from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app import models, schemas
from app.core.auth import get_password_hash, verify_password
from app.crud_v2.base import CRUDV2Base


class CRUDUser(
    CRUDV2Base[
        models.User,
        schemas.UserResponse,
        schemas.UserCreate,
        schemas.UserUpdate,
        schemas.UserResponse,
    ]
):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> models.User | None:
        stmt = select(models.User).where(models.User.email == email)
        return (await db.execute(stmt)).scalars().first()
        # return db.query(models.User).filter(models.User.email == email).first()

    async def create(self, db: AsyncSession, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(  # type: ignore[override]
        self, db: AsyncSession, *, db_obj: models.User, obj_in: schemas.UserUpdate
    ) -> models.User:
        if obj_in.password:
            hashed_password = get_password_hash(obj_in.password)
            db_obj.hashed_password = hashed_password
        return await super().update(db, db_obj=db_obj, update_schema=obj_in)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> models.User | None:
        user = await self.get_by_email(db, email=email)
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
