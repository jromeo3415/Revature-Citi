'''
Robopulse Command Center Day 5 
Authentication endpoints
'''

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_role
from app.models import User, UserRole
from app.schemas.user import Token, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login(
                    form_data: OAuth2PasswordRequestForm = Depends(),
                    db: AsyncSession = Depends(get_db)
                ) -> Token:
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    # verify password is correct
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # set our access token
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})

    return Token(
        username=user.username,
        role=user.role,
        access_token=access_token,
        token_type="bearer",
    )

# function to register a new user. This endpoint is protected by the require_role dependancy
# which will require the user to have the Fleet Admin role
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
                            payload: UserCreate,
                            db: AsyncSession = Depends(get_db),
                            _: User = Depends(require_role(UserRole.FLEET_ADMIN))
                        ) -> User:
    existing = await db.execute(select(User).where(func.lower(User.username) == func.lower(payload.username)))

    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{payload.username}' is already taken"
        )

    user = User(
        username = payload.username,
        hashed_password = hash_password(payload.password),
        role = payload.role
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user