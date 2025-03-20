from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from schemas.content import Content
from schemas.user import User, UserPatch, UserRoles


async def select_user_by_email(
        email: str, session: AsyncSession
) -> User | None:
    '''Получение пользователя по email'''
    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(user_create: dict, session: AsyncSession) -> User:
    '''Добавление пользователя'''
    user = User(**user_create)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def select_user_by_id(
        user_id: int, session: AsyncSession
) -> User | None:
    '''Получение пользователя по id'''
    return await session.get(User, user_id)


async def select_all_users(
        session: AsyncSession
) -> list[User] | None:
    stmt = select(User)
    '''Получение списка всех пользователей'''
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def patch_user(
        update_user: User, user_patch: UserPatch, session: AsyncSession
) -> User:
    '''Изменение роли пользователя'''
    update_user.sqlmodel_update(user_patch.model_dump())
    session.add(update_user)
    await session.commit()
    await session.refresh(update_user)
    return update_user


async def create_content(
        content_create: dict, session: AsyncSession
) -> Content:
    '''Добавление контента'''
    content = Content(**content_create)
    session.add(content)
    await session.commit()
    await session.refresh(content)
    return content


async def select_all_content(
        role: UserRoles, session: AsyncSession
) -> list[Content]:
    '''Получение списка всего контента'''
    if role == UserRoles.CLIENT:
        stmt = select(Content).where(Content.for_role == role)
    else:
        stmt = select(Content)
    result: Result = await session.execute(stmt)
    return result.scalars().all()
