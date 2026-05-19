import datetime

import jwt
from django.conf import settings


def create_access_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def get_user_id_from_request(request) -> int | None:
    auth_header = request.headers.get('Authorization', '')
    token = auth_header[7:].strip() if auth_header.startswith('Bearer ') else auth_header.strip()
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.PyJWTError:
        return None
    user_id = payload.get('user_id')
    return int(user_id) if user_id is not None else None
