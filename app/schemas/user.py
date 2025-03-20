from enum import Enum

from sqlmodel import Field, SQLModel


class UserRoles(str, Enum):
    ADMIN = 'admin'
    CLIENT = 'client'


class UserBase(SQLModel):
    email: str = Field(
        unique=True,
        index=True,
        nullable=False
    )


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: UserRoles = Field(default=UserRoles.CLIENT)
    hash_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: UserRoles


class UserPatch(SQLModel):
    role: UserRoles | None = None
