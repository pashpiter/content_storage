from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.validators import is_admin, is_one_user
from db.crud import patch_user, select_all_users, select_user_by_id
from db.database import get_session
from schemas.user import User, UserPatch, UserRead
from services.user import get_user, is_user

router = APIRouter(prefix='/users')


@router.get('')
async def get_users(
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_session)
) -> list[UserRead]:
    '''Получение списка всех пользователей'''
    await is_admin(user)
    users = await select_all_users(session)
    await is_one_user(users)
    return users


@router.patch('/{user_id}')
async def edit_user_role(
    user_id: int,
    user_patch: UserPatch,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_session)
) -> UserRead:
    '''Изменение роли пользователя'''
    await is_admin(user)
    update_user = await select_user_by_id(user_id, session)
    await is_user(update_user)
    user_new = await patch_user(update_user, user_patch, session)
    return user_new
