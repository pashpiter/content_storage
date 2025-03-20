from enum import Enum

from sqlmodel import SQLModel


class TokenList(str, Enum):
    BLACKLIST = 'blacklist'
    WHITELIST = 'whitelist'


class TokenBase(SQLModel):
    access_token: str


class TokenRead(TokenBase):
    pass
