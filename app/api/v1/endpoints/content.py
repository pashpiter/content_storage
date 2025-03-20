from fastapi import APIRouter, Depends, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.validators import is_admin
from db.crud import create_content, select_all_content
from db.database import get_session
from schemas.content import Content
from schemas.user import User, UserRoles
from services.content import save_file_to_disk
from services.user import get_user

router = APIRouter(prefix='/content')


@router.get('')
async def get_content(
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_session)
) -> list[Content]:
    '''Получение списка всего контента'''
    contents = await select_all_content(user.role, session)
    return contents


@router.post('')
async def add_content(
        file: UploadFile,
        title: str = Form(default=None),
        for_role: UserRoles = Form(default=UserRoles.CLIENT),
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_session)
) -> Content:
    '''Добавление контента'''
    await is_admin(user)
    file_path = await save_file_to_disk(file)
    content_dump = {
        'title': title if title else file.filename,
        'for_role': for_role,
        'file_path': file_path
    }
    content = await create_content(content_dump, session)
    return content
