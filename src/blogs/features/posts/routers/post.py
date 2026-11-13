from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from blogs.core.database import get_db
from blogs.features.posts.models import Post

router = APIRouter(prefix="/posts", tags=["posts"])


# Reusable database dependency type.
DbSession = Annotated[Session, Depends(get_db)]

# Session is a type/class definition provided by SQLAlchemy.
# Depends() is a FastAPI dependency injection function.
# It tells fastAPI before running this route, call get_db() and give me whatever it returns/yields.


@router.get("/")
def get_posts(db: DbSession):

    posts = db.query(Post).all()

    return posts


# @router.post("/")
# def create_post(post: Post, db: DbSession):
