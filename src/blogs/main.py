from fastapi import FastAPI

from blogs.comments.routers.comments import router as comments_router
from blogs.posts.routers.posts import router as posts_router
from blogs.tags.routers.tags import router as tags_router
from blogs.users.routers.users import router as users_router

app = FastAPI(title="Blogs API")

# Register routers
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(comments_router)
app.include_router(tags_router)

# Note: Database tables are managed by Alembic migrations (alembic upgrade head).
# Base.metadata.create_all(bind=engine) is no longer needed!
