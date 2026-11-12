from fastapi import FastAPI

# Import all models so they are registered with SQLAlchemy's Base metadata.
from blogs.comments.models import Comment  # noqa: F401
from blogs.comments.routers.comments import router as comments_router
from blogs.posts.models import Post  # noqa: F401
from blogs.posts.routers.posts import router as posts_router
from blogs.tags.models import PostTag, Tag  # noqa: F401
from blogs.tags.routers.tags import router as tags_router
from blogs.users.models import User  # noqa: F401
from blogs.users.routers.users import router as users_router
from core.database import Base, engine

app = FastAPI(title="Blogs API")

# Register routers
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(comments_router)
app.include_router(tags_router)

# Create all registered tables in the database if they don't exist.
Base.metadata.create_all(bind=engine)
