from typing import Annotated

from fastapi import APIRouter, Header

from app.api.models.currency import Currency
from app.utils.external_api import get_currency_list, convert

router = APIRouter(
    prefix="/currency",
    tags=["Currency"],

                   )


@router.get("/list")
async def list_currency():
    currency_list = get_currency_list()
    return {"status": 200, "currencies": currency_list}


@router.post("/convert")
async def convert_currency(request: Currency):
    result = convert(request.amount, request.convert_from, request.convert_to)
    return {"status": 200, "result": result}


@router.get("/items")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
