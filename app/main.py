from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.v1 import router as v1_router
from core.config import STATIC
from db.database import create_tables_and_admin_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables_and_admin_user()
    yield


app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory=STATIC), name='static')
app.include_router(v1_router)
