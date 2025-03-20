from sqlmodel import Field, SQLModel

from schemas.user import UserRoles


class ContentBase(SQLModel):
    title: str | None = None
    for_role: UserRoles = Field(default=UserRoles.CLIENT)


class Content(ContentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_path: str | None


class ContentCreate(ContentBase):
    pass


class ContentRead(ContentBase):
    file_path: str | None
