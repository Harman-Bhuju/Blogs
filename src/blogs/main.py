from fastapi import FastAPI

from blogs.features.comments.routers.comment import router as comments_router
from blogs.features.posts.routers.post import router as posts_router
from blogs.features.tags.routers.tags import router as tags_router
from blogs.features.users.routers.user import router as users_router
from blogs.models import register_models

# Ensure all SQLAlchemy models and mappers are configured at application startup.
register_models()

app = FastAPI(title="Blogs API")

# Register routers
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(comments_router)
app.include_router(tags_router)

# Note: Database tables are managed by Alembic migrations (alembic upgrade head).
# Base.metadata.create_all(bind=engine) is no longer needed!
