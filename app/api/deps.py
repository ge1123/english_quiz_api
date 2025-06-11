from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from jose import JWTError
from app.utils.jwt_helper import decode_token

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user(token: str = Security(api_key_header)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token or not token.startswith("Bearer "):
        raise credentials_exception

    try:
        token = token[7:]
        payload = decode_token(token)
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
