from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
from starlette.templating import Jinja2Templates

from app.api.endpoints.currency import router
from app.api.endpoints.jwt import user_router

app = FastAPI()

app.include_router(router)
app.include_router(user_router)