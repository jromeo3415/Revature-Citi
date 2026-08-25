'''
Day 4 - Shared fastAPI dependencies

Day 5 - Adding get_current_user and require_role
'''

from collections.abc import AsyncGenerator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import AsyncSessionLocal
from app.models import User, UserRole
from app.security import decode_access_token

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# create a dependency that will extract the current user from the JWT token
# which is provided in the auth header of the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
    ) -> User: 

    # we will use the decode_access_token function to decode the JWT token 
    # and extract the username from the payload. we also want to catch any 
    # exceptions that may occur during this process
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload=decode_access_token(token)

        # sub is the standard claim name for the subject of the token
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

# need a dependency that checks if the current user has the required role(s)
# required to access a certain route
def require_role(*allowed_roles: UserRole):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Role {current_user.role.value} is not permitted to perform this action"
                )
            )

        return current_user

    return role_checker