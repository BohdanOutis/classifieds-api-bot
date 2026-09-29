from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from .config import config

X_API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(X_API_KEY_HEADER)):

    expected_key = config.api.server_secret_key.get_secret_value()

    if not api_key or api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid or missing X-API-Key header"
        )
    return api_key