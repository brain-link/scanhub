# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data access layer."""

from pprint import pprint

from api.db import Exam, Job, Procedure, Record, async_session
from api.models import BaseExam, BaseJob, ProcedureIn, RecordIn
from sqlalchemy.engine import Result
from sqlalchemy.future import select


async def exam_add(payload: BaseExam) -> Exam:
    """Add a new exam to the database.

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


async def exam_get(exam_id: int) -> (Exam | None):
    """Fetch an exam from database.

    Arguments:
        id {int} -- Identifier of exam

    Returns:
        Exam -- Database orm model
    """
    async with async_session() as session:
        exam: (Exam | None) = await session.get(Exam, exam_id)
    return exam


async def exam_get_all(patient_id: int) -> list[Exam]:
    """Fetch all exams which belong to a patient.

    Arguments:
        patient_id {str} -- ID of associated patient

    Returns:
        List[Exam] -- List of database orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Exam).where(Exam.patient_id == patient_id))
        exams = list(result.scalars().all())
    return exams


async def exam_delete(exam_id: int) -> bool:
    """Delete an exam by ID.

    Arguments:
        id {int} -- ID of exam to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        if (exam := await session.get(Exam, exam_id)):
            await session.delete(exam)
            await session.commit()
            return True
        return False


async def update_exam(exam_id: int, payload: BaseExam) -> (Exam | None):
    """Update an existing exam in database.

    Arguments:
        id {int} -- ID of exam
        payload {BaseWorkflow} -- Pydantic base model, data to be updated

    Returns:
        Workflow -- Updated database orm model
    """
    async with async_session() as session:
        if (exam := await session.get(Exam, exam_id)):
            exam.update(payload.dict())
            await session.commit()
            await session.refresh(exam)
            return exam
        return None


async def procedure_add(payload: ProcedureIn) -> Procedure:
    """Add a new procedure to the database.

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


async def procedure_get(procedure_id: int) -> (Procedure | None):
    """Fetch a procedure from database.

    Arguments:
        id {int} -- ID of procedure

    Returns:
        Procedure -- Database orm model
    """
    async with async_session() as session:
        procedure: (Procedure | None) = await session.get(Procedure, procedure_id)
    return procedure


async def procedure_get_all(exam_id: int) -> list[Procedure]:
    """Fetch all procedures of an exam.

    Arguments:
        exam_id {int} -- ID of exam

    Returns:
        list[Procedure] -- List of database orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Procedure).where(Procedure.exam_id == exam_id))
        procedures = list(result.scalars().all())
    return procedures


async def procedure_delete(procedure_id: int) -> bool:
    """Delete a procedure by ID.

    Arguments:
        id {int} -- ID of procedure to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        if (procedure := await session.get(Procedure, procedure_id)):
            await session.delete(procedure)
            await session.commit()
            return True
        return False


async def procedure_update(procedure_id: int, payload: ProcedureIn) -> (Procedure | None):
    """Update an existing procedure in database.

    Arguments:
        id {int} -- ID of procedure
        payload {BaseProcedure} -- Pydantic base model, data to be updated

    Returns:
        Procedure -- Updated database orm model
    """
    async with async_session() as session:
        if (procedure := await session.get(Procedure, procedure_id)):
            procedure.update(payload.dict())
            await session.commit()
            await session.refresh(procedure)
            return procedure
        return None


# **************************************************
# Jobs
# **************************************************

async def add_job(payload: BaseJob) -> Job:
    """Add a new job to the database.

    Arguments:
        payload {BaseJob} -- Pydantic model to create a new database entry

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


async def get_job(job_id: int) -> (Job | None):
    """Fetch a job from database.

    Arguments:
        id {int} -- ID of job

    Returns:
        Job -- Database orm model
    """
    async with async_session() as session:
        job: (Job | None) = await session.get(Job, job_id)
    return job


async def get_all_jobs(procedure_id: int) -> list[Job]:
    """Fetch all jobs of a record.

    Arguments:
        id {int} -- ID of job

    Returns:
        Job -- Database orm model
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Job).where(Job.procedure_id == procedure_id))
        jobs = list(result.scalars().all())
    return jobs


async def delete_job(job_id: int) -> bool:
    """Delete a job by ID.

    Arguments:
        id {int} -- ID of job to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        if (job := await session.get(Job, job_id)):
            await session.delete(job)
            await session.commit()
            return True
        return False


async def update_job(job_id: int, payload: BaseJob) -> (Job | None):
    """Update an existing job in database.

    Arguments:
        id {int} -- ID of job
        payload {BaseJob} -- Pydantic base model, data to be updated

    Returns:
        Job -- Updated database orm model
    """
    async with async_session() as session:
        if (job := await session.get(Job, job_id)):
            job.update(payload.dict())
            await session.commit()
            await session.refresh(job)
            return job
        return None


# **************************************************
# RECORDS
# **************************************************

async def add_record(payload: RecordIn) -> Record:
    """Add a new record to the database.

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


async def get_record(record_id: int) -> (Record | None):
    """Fetch a record from database.

    Arguments:
        id {int} -- ID of record

    Returns:
        Record -- Database orm model
    """
    async with async_session() as session:
        record: (Record | None) = await session.get(Record, record_id)
    return record


async def get_all_records(job_id: int) -> list[Record]:
    """Fetch all records of a job.

    Arguments:
        id {int} -- ID of record

    Returns:
        Record -- Database orm model
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Record).where(Record.job_id == job_id))
        records = list(result.scalars().all())
    return records


async def delete_record(record_id: int) -> bool:
    """Delete a record by ID.

    Arguments:
        id {int} -- ID of record to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        if (record := await session.get(Record, record_id)):
            await session.delete(record)
            await session.commit()
            return True
        return False
