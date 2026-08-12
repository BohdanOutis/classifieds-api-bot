from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext

SECRET_KEY = "YOUR_SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: int, role: str) -> str:
    payload = {"sub": str(user_id), "role": role}
    return create_token(payload, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access")

def create_refresh_token(user_id: int) -> str:
    payload = {"sub": str(user_id)}
    return create_token(payload, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), "refresh")

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None