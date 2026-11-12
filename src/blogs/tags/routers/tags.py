from fastapi import APIRouter

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/")
def get_tags():
    return []
