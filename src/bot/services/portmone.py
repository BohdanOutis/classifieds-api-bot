import os 
import hashlib
import urllib.parse
from typing import Dict

PORTMONE_PAYEE_ID = os.environ("PORTMONE_PAYEE_ID")
PORTMONE_SECRET_KEY = os.environ("PORTMONE_SECRET_KEY")
PORTMONE_GATEWAY_URL = os.environ("PORTMONE_GATEWAY_URL")

WEBHOOK_SUCCESS_URL = ""
WEBHOOK_FAILURE_URL = ""

def generate_portmone_signature(payee_id: str, shop_order_number: str, amount: str, secret_key: str) -> str:
    raw_str = f"{payee_id}{shop_order_number}{amount}{secret_key}"
    return hashlib.md5(raw_str.encode('utf-8')).hexdigest().upper()


def get_portomne_payment_link(
    shop_order_number: str,
    amount: float,
    description: str
) -> str:
    str_amount = f"{amount:.2f}"

    signature = generate_portmone_signature(
        payee_id=PORTMONE_PAYEE_ID,
        shop_order_number=shop_order_number,
        amount=amount,
        secret_key=PORTMONE_SECRET_KEY
    )

    params = {
        "payee_id": PORTMONE_PAYEE_ID,
        "shop_order_number": shop_order_number,
        "bill_amount": str_amount,
        "description": description,
        "success_url": WEBHOOK_SUCCESS_URL,
        "failure_url": WEBHOOK_FAILURE_URL,
        "encoding": "UTF-8",
        "cms_name": "python_aiogram_bot",
        "signature": signature
    }

    return f"{PORTMONE_GATEWAY_URL}?{urllib.parse.urlencode(params)}"