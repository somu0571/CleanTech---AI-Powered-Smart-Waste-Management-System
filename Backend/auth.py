"""
auth.py – JWT creation / verification + password hashing
(FINAL WITH ADMIN + RECYCLER ROLE SUPPORT)
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# ── Config ────────────────────────────────────────────────────────────────────

SECRET_KEY = os.getenv("SECRET_KEY", "cleantech-super-secret-key-change-in-prod")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 8   # 8 hours

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ── Password helpers ──────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


# ── JWT helpers ───────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ── FastAPI dependency ────────────────────────────────────────────────────────

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_token(token)

    username: str = payload.get("sub")
    role: str = payload.get("role")
    user_id = payload.get("id")

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return {
        "username": username,
        "role": role,
        "id": user_id
    }


# ── Role Guards ───────────────────────────────────────────────────────────────

def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


def require_citizen(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] not in ("citizen", "admin"):
        raise HTTPException(status_code=403, detail="Citizen access required")
    return current_user


# ✅ NEW: Recycler Access Control
def require_recycler(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] not in ("recycler", "admin"):
        raise HTTPException(status_code=403, detail="Recycler access required")
    return current_user