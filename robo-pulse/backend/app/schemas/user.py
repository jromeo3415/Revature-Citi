'''
Robopulse Command Center Day 5
Pydantic v2 schemas for the User and auth resources
'''

from pydantic import BaseModel, ConfigDict, Field

from app.models import UserRole

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    role: UserRole

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)

# we are not adding the password field to the user read schema since
# we do not want to expose the hashed password in our API responses
class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Token(UserBase):
    access_token: str
    token_type: str = "bearer"

