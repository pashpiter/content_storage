from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, insert, select

from core.config import settings
# from schemas.content import Content
from schemas.user import User, UserRoles


async_engine = create_async_engine(
    settings.postgres.postgres_url, echo=settings.app.debug
)

async_session_factory = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_tables_and_admin_user() -> None:
    '''Создание таблиц и добавление админа'''
    from services.user import create_hashed_password
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        admin_db = await conn.execute(select(User).where(
            User.email == settings.app.admin_email,
            User.role == UserRoles.ADMIN
        ))
        admin = admin_db.one_or_none()
        if admin:
            return
        stmt = insert(User).values(
            email=settings.app.admin_email,
            hash_password=await create_hashed_password(
                settings.app.admin_password
            ),
            role=UserRoles.ADMIN
        )
        await conn.execute(stmt)
        await conn.commit()


async def get_session():
    '''Session с БД'''
    async with async_session_factory() as session:
        yield session
