# Data Access Layer

from api.models import BaseExam, ExamOut, get_exam_out
from api.models import ProcedureIn, ProcedureOut, get_procedure_out
from api.db import Exam, Procedure, Record, async_session
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pprint import pprint
from sqlalchemy.dialects.postgresql import UUID


async def add_exam(payload: BaseExam) -> ExamOut:
    new_exam = Exam(**payload.dict())
    async with async_session() as session:
        session.add(new_exam)
        await session.commit()
        await session.refresh(new_exam)
    print("***** NEW UUID: ", new_exam.id)
    return await get_exam_out(new_exam)

async def get_exam(id: str) -> ExamOut:
    async with async_session() as session:
        exam = await session.get(Exam, id)
        # await session.refresh(exam, "procedures")

        # print(exam.procedures)
        # exam = await session.execute(select(Exam).where(Exam.id == id).options(selectinload(Exam.procedures)))
        # await exam.options(selectinload(Exam.procedures))
        # exam = await result.options(selectinload(Exam.procedures))
        # exam = await session.execute(select(Exam).get(id).options(selectinload(Exam.procedures)))
        
        # stmt = select(Exam).where(Exam.id == id)
        # stmt = stmt.options(selectinload(Exam.procedures))
        # exam = await session.scalar(stmt)

        pprint(exam.__dict__)

        # exam_out = await get_exam_out(exam)
        # pprint(exam_out)
        # return exam_out

async def get_exams(patient_id: str) -> ExamOut:
    async with async_session() as session:
        result = await session.execute(select(Exam).where(Exam.patient_id == patient_id))
        exams = result.scalars().all()
        return [await get_exam_out(exam) for exam in exams]

# async def delete_exam(id: int):
#     query = exam.delete(exam.c.id==id).where()
#     return await database.fetch_one(query=query)

# async def update_exam(id: int, payload: BaseExam):
#     query = exam.update(exam.c.id==id).values(**payload.dict())
#     return await database.execute(query=query)


async def add_procedure(payload: ProcedureIn) -> ProcedureOut:
    exam_id = payload.exam_id
    new_procedure = Procedure(**payload.dict())
    async with async_session() as session:
        new_procedure.exam = await session.get(Exam, exam_id)
        session.add(new_procedure)
        await session.commit()
        await session.refresh(new_procedure)
    print("***** NEW PROCEDURE UUID: ", new_procedure.id)
    pprint(new_procedure.__dict__)
    response = await get_procedure_out(new_procedure)
    # pprint(response.dict())
    return response

async def get_procedure(id: str) -> ProcedureOut:
    async with async_session() as session:
        procedure = await session.get(Procedure, id)
        await session.refresh(Procedure, "exam")
        print("****** TEST: ", procedure.exam)
        return await get_procedure_out(procedure)
    
async def get_procedures(exam_id: str) -> list[ProcedureOut]:
    async with async_session() as session:
        result = await session.execute(select(Procedure).where(Procedure.exam_id == exam_id))
        procedures = result.scalars().all()
        return [await get_procedure_out(procedure) for procedure in procedures]