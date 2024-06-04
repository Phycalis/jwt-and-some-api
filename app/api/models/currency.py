from pydantic import BaseModel


class Currency(BaseModel):
    convert_from: str
    convert_to: str
    amount: int
