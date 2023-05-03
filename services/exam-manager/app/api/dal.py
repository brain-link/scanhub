# Data Access Layer (DAL)

from sqlalchemy.future import select
from typing import List
from pprint import pprint

from api.models import BaseExam, ProcedureIn, JobIn, RecordIn  # pydantic models
from api.db import Exam, Procedure, Job, Record, async_session   # database orm models


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


async def get_all_exams(patient_id: int) -> List[Exam]:
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
    if exam:
        exam.update(payload.dict())
        await session.commit()
        await session.refresh(exam)
        return exam
    else:
        return None


# **************************************************
# PROCEDURES
# **************************************************

async def add_procedure(payload: ProcedureIn) -> Procedure:
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
        
    
async def update_procedure(id: int, payload: ProcedureIn) -> Procedure:
    """Update an existing procedure in database

    Arguments:
        id {int} -- ID of procedure
        payload {BaseProcedure} -- Pydantic base model, data to be updated

    Returns:
        Procedure -- Updated database orm model
    """
    async with async_session() as session:
        procedure = await session.get(Procedure, id)
        if procedure:
            procedure.update(payload.dict())
            await session.commit()
            await session.refresh(procedure)
            return procedure
        else:
            return None


# **************************************************
# Jobs
# **************************************************

async def add_job(payload: JobIn) -> Job:
    """Add a new job to the database

    Arguments:
        payload {JobIn} -- Pydantic model to create a new database entry

    Returns:
        Job -- Database orm model
    """
    new_job = Job(**payload.dict())
    async with async_session() as session:
        session.add(new_job)
        await session.commit()
        await session.refresh(new_job)
    # Debugging
    print("***** NEW JOB *****")
    pprint(new_job.__dict__)
    return new_job


async def get_job(id: int) -> Job:
    """Fetch a job from database

    Arguments:
        id {int} -- ID of job

    Returns:
        Job -- Database orm model
    """
    async with async_session() as session:
        job = await session.get(Job, id)
    return job


async def get_all_jobs(procedure_id: int) -> list[Job]:
    """Fetch all jobs of a record

    Arguments:
        id {int} -- ID of job

    Returns:
        Job -- Database orm model
    """
    async with async_session() as session:
        result = await session.execute(select(Job).where(Job.procedure_id == procedure_id))
        jobs = result.scalars().all()
    return jobs


async def delete_job(id: int) -> bool:
    """Delete a job by ID

    Arguments:
        id {int} -- ID of job to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        job = await session.get(Job, id)
        if job:
            await session.delete(job)
            await session.commit()
            return True
        else: 
            return False


async def update_job(id: int, payload: JobIn) -> Job:
    """Update an existing job in database

    Arguments:
        id {int} -- ID of job
        payload {JobIn} -- Pydantic base model, data to be updated

    Returns:
        Job -- Updated database orm model
    """
    async with async_session() as session:
        job = await session.get(Job, id)
        if job:
            job.update(payload.dict())
            await session.commit()
            await session.refresh(job)
            return job
        else:
            return None


# **************************************************
# RECORDS
# **************************************************

async def add_record(payload: RecordIn) -> Record:
    """Add a new record to the database

    Arguments:
        payload {RecordIn} -- Pydantic model to create a new database entry

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
        record = await session.get(Record, id)
    return record


async def get_all_records(job_id: int) -> list[Record]:
    """Fetch all records of a job

    Arguments:
        id {int} -- ID of record

    Returns:
        Record -- Database orm model
    """
    async with async_session() as session:
        result = await session.execute(select(Record).where(Record.job_id == job_id))
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
