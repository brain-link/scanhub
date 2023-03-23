# data access layer (DAL)

from sqlalchemy.future import select
from sqlalchemy import update
from pprint import pprint
from typing import List

from api.models import BaseWorkflow, WorkflowOut, get_workflow_out
from api.db import Workflow, async_session



async def add_workflow(payload: BaseWorkflow) -> WorkflowOut:
    new_workflow = Workflow(**payload.dict())
    async with async_session() as session:
        session.add(new_workflow)
        await session.commit()
        await session.refresh(new_workflow)
    print("***** NEW WORKFLOW *****")
    pprint(new_workflow.__dict__)
    return await get_workflow_out(new_workflow)


async def get_workflow(id: int) -> WorkflowOut:
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
    return await get_workflow_out(workflow)


async def get_all_workflows() -> List[WorkflowOut]:
    async with async_session() as session:
        result = await session.execute(select(Workflow))
        workflows = result.scalars().all()
    return [await get_workflow_out(workflow) for workflow in workflows]


async def delete_workflow(id: int) -> bool:
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
        if workflow:
            await session.delete(workflow)
            await session.commit()
            return True
        else: 
            return False
        # TODO: What to return here?


async def update_workflow(id: int, payload: BaseWorkflow) -> WorkflowOut:
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
        workflow.update(payload.dict())
        await session.commit()
        await session.refresh(workflow)

        # # Chat gpt suggestion:
        # stmt = update(Workflow).where(Workflow.id == id)
        # stmt.values(**payload.dict()) 
        # workflow = await session.execute(stmt)
        # await session.commit()
        
    return await get_workflow_out(workflow)




# Chat GPT example:

# from fastapi import FastAPI, HTTPException
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, selectinload
# from sqlalchemy.sql.expression import update, delete
# from sqlalchemy.exc import IntegrityError
# from pydantic import BaseModel
# from typing import Optional

# app = FastAPI()

# DATABASE_URL = "postgresql+asyncpg://user:password@host:port/dbname"

# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# class UserCreate(BaseModel):
#     name: str
#     email: str


# class UserUpdate(BaseModel):
#     name: Optional[str] = None
#     email: Optional[str] = None


# class User(BaseModel):
#     id: int
#     name: str
#     email: str


# @app.post("/users")
# async def create_user(user_create: UserCreate):
#     async with async_session() as session:
#         try:
#             user = User(name=user_create.name, email=user_create.email)
#             session.add(user)
#             await session.commit()
#             await session.refresh(user)
#             return user
        
#         except IntegrityError:
#             raise HTTPException(status_code=400, detail="Email already exists")


# @app.get("/users/{user_id}")
# async def get_user(user_id: int):
#     async with async_session() as session:
#         result = await session.execute(select(User).where(User.id == user_id))
#         user = result.scalar()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user


# @app.put("/users/{user_id}")
# async def update_user(user_id: int, user_update: UserUpdate):
#     async with async_session() as session:
#         try:
#             stmt = update(User).where(User.id == user_id)
#             if user_update.name:
#                 stmt = stmt.values(name=user_update.name)
#             if user_update.email:
#                 stmt = stmt.values(email=user_update.email)

#             result = await session.execute(stmt)
#             await session.commit()

#             if result.rowcount == 0:
#                 raise HTTPException(status_code=404, detail="User not found")
            
#             return {"message": "User updated successfully"}
        
#         except IntegrityError:
#             raise HTTPException(status_code=400, detail="Email already exists")


# @app.delete("/users/{user_id}")
# async def delete_user(user_id: int):
#     async with async_session() as session:
#         result = await session.execute(delete(User).where(User.id == user_id))
#         await session.commit()
#         if result.rowcount == 0:
#             raise HTTPException(status_code=404, detail="User not found")
#         return {"message": "User deleted successfully"}
