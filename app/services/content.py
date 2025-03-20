import os

from fastapi import UploadFile

from core.config import FILES, FILES_DIR, STATIC


async def save_file_to_disk(file: UploadFile) -> str:
    '''Сохранение фала на диск'''
    file_name = file.filename
    file_path = os.path.join(FILES_DIR, file_name)

    with open(file_path, "wb") as tmp:
        content = file.file.read()
        tmp.write(content)

    return f'/{STATIC}/{FILES}/{file_name}'
