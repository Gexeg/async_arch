from fastapi import FastAPI, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from domain.models import UserRole, User
from commands.register_user import register_user
from commands.create_token import create_token
from commands.get_user_by_token import get_user_by_token
from commands.update_user import update_user_role


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.ADMIN


@app.post("/super_secret_route/add_user")
async def add_new_user(create_user_data: CreateUserRequest = Body(...)):
    new_user = await register_user(**create_user_data.model_dump())
    if new_user is None:
        raise HTTPException(
            status_code=400, detail="User with this name already registered"
        )
    return new_user.model_dump()


class UpdateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.ADMIN


@app.put("/super_secret_route/update_user", response_model=User)
async def update_user(user_id: str, new_role: UserRole):
    user = await update_user_role(user_id, new_role)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user by id",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.put("/super_secret_route/delete_user", status_code=204)
async def update_user(user_id: str):
    await update_user_role(user_id)


class UserAuthN(BaseModel):
    name: str
    password: str


@app.post("/token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = await create_token(form_data.username, form_data.password)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/get_user", response_model=User)
async def get_token(token: str = Depends(oauth2_scheme)):
    user = await get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
