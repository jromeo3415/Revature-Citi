'''
Robopulse Command Center Day 5
Password hashing and JWT helper functions

SECRET-KEY: It follows the same env-var-with-fallback pattern that we saw on Day 3's DATABASE_URL
'''

import os 
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

# Security constants and helper functions for password hashing and JWT token management

SECRET_KEY = os.environ.get("SECRET_KEY", "<replace-with-a-real-secret-key>")

# using HS256 for hashing
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# takes a plain text password as input, hashes it using bcrpyt,
# and returns the hashed password as a string
def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

# takes a hashed password and a plain text password as input and 
# checks if the plain text password matches the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# creates a JWT access token with the provided data and an 
# optional expiration time
def create_access_token(data: dict, exprires_delta: timedelta | None = None) -> str:

    # copy of the input data dictionary which will be used to create the payload of the JWT
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        exprires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# decodes a JWT access token and returns the payload as a dictionary
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])