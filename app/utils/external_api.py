import requests

from app.core.config import AppConfig

config = AppConfig()


def get_currency_list():
    response = requests.get(f'{config.BASE_URL}/symbols', headers={"apikey": config.API_KEY})
    return response.json().get("symbols")


def convert(amount: int, from_curr: str, to_curr: str):
    response = requests.get(
        f'{config.BASE_URL}/convert',
        headers={"apikey": config.API_KEY},
        params={"to": to_curr, "from": from_curr, "amount": amount}
    )
    return response.json().get("result")


