import asyncio
from fastapi import FastAPI, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from domain.models import User, Task
from adapters.auth_client import AuthService
from commands.create_task import create_new_task
from commands.complete_task import complete_task
from commands.get_user_tasks import get_user_task
from commands.assign_tasks import assign_tasks
from adapters.broker_consumer import consumer


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@app.post("/create_task", response_model=Task)
async def create_task(
    user: User = Depends(get_user_data), task_data: CreateTaskRequest = Body(...)
):
    new_task = await create_new_task(user, task_data.description)
    if new_task is None:
        raise HTTPException(status_code=400, detail="Something went wrong")
    return new_task


@app.put("/complete_task", response_model=Task)
async def create_task(user: User = Depends(get_user_data), task_id: str = Body(...)):
    task = await complete_task(user, task_id)
    if task is None:
        raise HTTPException(status_code=400, detail="Something went wrong")
    return task


@app.get("/get_my_tasks")
async def create_task(user: User = Depends(get_user_data)):
    task = await get_user_task(user)
    if task is None:
        raise HTTPException(status_code=400, detail="Something went wrong")
    return task


@app.get("/get_my_tasks")
async def create_task(user: User = Depends(get_user_data)):
    task = await get_user_task(user)
    if task is None:
        raise HTTPException(status_code=400, detail="Something went wrong")
    return task


@app.get("/assign_tasks")
async def create_task(user: User = Depends(get_user_data)):
    await assign_tasks(user)
