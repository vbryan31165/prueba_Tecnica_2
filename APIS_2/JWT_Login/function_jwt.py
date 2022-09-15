from jwt import encode, decode
from jwt import exceptions
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify


def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date


def write_token(data: dict):
    print("inicio")
    print(data)
    print("-----")
    token = encode(payload={**data, "exp": expire_date(2)}, key="1234", algorithm="HS256")
    return token.encode("UTF-8")


def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key="1234", algorithms="HS256")
        decode(token, key="1234", algorithms="HS256")
    except exceptions.DecodeError:
        response = jsonify("message", "Invalid token")
        response.status_code = 400
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify("message", "Token expired")
        response.status_code = 400
        return response