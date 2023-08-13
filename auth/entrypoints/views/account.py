from fastapi import FastAPI, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from entrypoints.views.request_models import CreateUserRequest
from commands.register_user import register_user
from commands.create_token import create_token


app = FastAPI()


@app.post("/super_secret_route/add_user")
async def add_new_user(create_user_data: CreateUserRequest = Body(...)):
    new_user = await register_user(**create_user_data.model_dump())
    if new_user is None:
        raise HTTPException(status_code=400, detail="User with this name already registered")
    return new_user.model_dump()


@app.post("/token")
async def add_new_user(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = await create_token(form_data.username, form_data.password)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": access_token, "token_type": "bearer"}
