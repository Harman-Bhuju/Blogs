from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from blogs.core.database import get_db
from blogs.features.users.models import User as UserModel
from blogs.features.users.schemas import User as UserSchema

router = APIRouter(prefix="/users", tags=["users"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/")
async def get_users( db: DbSession):
    statement = select(UserModel)
    result = db.execute(statement)
    users = result.first()
    return users

@router.post("/")
async def create_user(user: UserSchema, db: DbSession):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user