import asyncio
from fastapi import FastAPI, Depends, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from adapters.auth_client import AuthService
from adapters.broker_consumer import consumer
from settings import settings
from commands.count_account import count_account
from commands.get_my_account import get_my_account


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"http:{settings.auth_service_host}:{settings.auth_service_port}/token"
)


@app.on_event("startup")
async def startup_event():
    await consumer.start()
    asyncio.create_task(consumer.consume())


@app.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()


class CreateTaskRequest(BaseModel):
    description: str


async def get_user_data(token: str = Depends(oauth2_scheme)):
    auth_client = AuthService()
    user = await auth_client.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/count_account/{user_id}")
async def count_user_account(user_id: int = Path(...)):
    return await count_account(user_id)


@app.put("/get_my_account")
async def get_user_account(user_id: int = Query(...)):
    return await get_my_account(user_id)
