# Data Access Layer (DAL)

from sqlalchemy.future import select
from typing import List
from pprint import pprint

from api.models import BaseExam, BaseProcedure, BaseRecord  # pydantic models
from api.db import Exam, Procedure, Record, async_session   # database orm models



# **************************************************
# EXAMS
# **************************************************

async def add_exam(payload: BaseExam) -> Exam:
    """Add a new exam to the database

    Arguments:
        payload {BaseExam} -- Pydantic base model to create a new database entry

    Returns:
        Exam -- Database orm model
    """
    new_exam = Exam(**payload.dict())
    async with async_session() as session:
        session.add(new_exam)
        await session.commit()
        await session.refresh(new_exam)
    # debug
    print("***** NEW EXAM *****")
    pprint(new_exam.__dict__)
    return new_exam


async def get_exam(id: int) -> Exam:
    """Fetch an exam from database

    Arguments:
        id {int} -- Identifier of exam

    Returns:
        Exam -- Database orm model
    """
    async with async_session() as session:
        exam = await session.get(Exam, id)
    return exam


async def get_all_exams(patient_id: str) -> List[Exam]:
    """Fetch all exams which belong to a patient

    Arguments:
        patient_id {str} -- ID of associated patient

    Returns:
        List[Exam] -- List of database orm models
    """
    async with async_session() as session:
        result = await session.execute(select(Exam).where(Exam.patient_id == patient_id))
        exams = result.scalars().all()
    return exams


async def delete_exam(id: int) -> bool:
    """Delete an exam by ID

    Arguments:
        id {int} -- ID of exam to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        exam = await session.get(Exam, id)
        if exam:
            await session.delete(exam)
            await session.commit()
            return True
        else: 
            return False
        

async def update_exam(id: int, payload: BaseExam) -> Exam:
    """Update an existing exam in database

    Arguments:
        id {int} -- ID of exam
        payload {BaseWorkflow} -- Pydantic base model, data to be updated

    Returns:
        Workflow -- Updated database orm model
    """
    async with async_session() as session:
        exam = await session.get(Exam, id)
        exam.update(payload.dict())
        await session.commit()
        await session.refresh(exam)
    return exam


# **************************************************
# PROCEDURES
# **************************************************

async def add_procedure(payload: BaseProcedure) -> Procedure:
    """Add a new procedure to the database

    Arguments:
        payload {BaseProcedure} -- Pydantic base model to create a new database entry

    Returns:
        Procedure -- Database orm model
    """
    new_procedure = Procedure(**payload.dict())
    async with async_session() as session:
        session.add(new_procedure)
        await session.commit()
        await session.refresh(new_procedure)
    # debug
    print("***** NEW PROCEDURE *****")
    pprint(new_procedure.__dict__)
    return new_procedure


async def get_procedure(id: int) -> Procedure:
    """Fetch a procedure from database

    Arguments:
        id {int} -- ID of procedure

    Returns:
        Procedure -- Database orm model
    """
    async with async_session() as session:
        procedure = await session.get(Procedure, id)
    return procedure
    

async def get_all_procedures(exam_id: int) -> list[Procedure]:
    """Fetch all procedures of an exam

    Arguments:
        exam_id {int} -- ID of exam

    Returns:
        list[Procedure] -- List of database orm models
    """
    async with async_session() as session:
        result = await session.execute(select(Procedure).where(Procedure.exam_id == exam_id))
        procedures = result.scalars().all()
    return procedures
    

async def delete_procedure(id: int) -> bool:
    """Delete a procedure by ID

    Arguments:
        id {int} -- ID of procedure to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        procedure = await session.get(Procedure, id)
        if procedure:
            await session.delete(procedure)
            await session.commit()
            return True
        else: 
            return False
        
    
async def update_procedure(id: int, payload: BaseProcedure) -> Procedure:
    """Update an existing procedure in database

    Arguments:
        id {int} -- ID of procedure
        payload {BaseProcedure} -- Pydantic base model, data to be updated

    Returns:
        Procedure -- Updated database orm model
    """
    async with async_session() as session:
        procedure = await session.get(Procedure, id)
        procedure.update(payload.dict())
        await session.commit()
        await session.refresh(procedure)
    return procedure


# **************************************************
# RECORDS
# **************************************************

async def add_record(payload: BaseRecord) -> Record:
    """Add a new record to the database

    Arguments:
        payload {BaseRecord} -- Pydantic base model to create a new database entry

    Returns:
        Record -- Database orm model
    """
    new_record = Record(**payload.dict())
    async with async_session() as session:
        session.add(new_record)
        await session.commit()
        await session.refresh(new_record)
    # Debugging
    print("***** NEW RECORD *****")
    pprint(new_record.__dict__)
    return new_record


async def get_record(id: int) -> Record:
    """Fetch a record from database

    Arguments:
        id {int} -- ID of record

    Returns:
        Record -- Database orm model
    """
    async with async_session() as session:
        workflow = await session.get(Record, id)
    return workflow


async def get_all_records(procedure_id: int) -> List[Record]:
    """Fetch all exams which belong to a procedure

    Returns:
        List[Procedure] -- List of database orm models
    """
    async with async_session() as session:
        result = await session.execute(select(Record).where(Record.procedure_id == procedure_id))
        records = result.scalars().all()
    return records


async def delete_record(id: int) -> bool:
    """Delete a record by ID

    Arguments:
        id {int} -- ID of record to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        record = await session.get(Record, id)
        if record:
            await session.delete(record)
            await session.commit()
            return True
        else: 
            return False


async def update_record(id: int, payload: BaseRecord) -> Record:
    """Update an existing record in database

    Arguments:
        id {int} -- ID of record
        payload {BaseRecord} -- Pydantic base model, data to be updated

    Returns:
        Record -- Updated database orm model
    """
    async with async_session() as session:
        record = await session.get(Record, id)
        record.update(payload.dict())
        await session.commit()
        await session.refresh(record)
    return record
