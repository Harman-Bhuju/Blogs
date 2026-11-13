from pydantic import BaseModel, ConfigDict, Field
from pydantic.experimental.missing_sentinel import MISSING

from blogs.features.users.schemas import User


# Common fields inherited by other post models.
class PostBase(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    published: bool = True
    rating: int | None = None
    author: User | None = None
    tags: list[str] = Field(default_factory=list)

# POST: Create a post.
class CreatePost(PostBase):
    pass

# PATCH: Update selected fields.
class PostUpdate(PostBase):
    title: str | MISSING = Field(default=MISSING, min_length=1)
    content: str | MISSING = Field(default=MISSING, min_length=1)
    published: bool | MISSING = MISSING
    rating: int | None | MISSING = MISSING
    author: User | None | MISSING = MISSING
    tags: list[str] | MISSING = MISSING

# Query parameter model.
class PostFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")  
    
    limit: int = Field(default=10, gt = 0 , le = 100)  

    published: bool = True

    search: str | None = Field(
        default= None,
        min_length=3,
        max_length = 50)

    tags: list[str] = Field(default_factory= list) 