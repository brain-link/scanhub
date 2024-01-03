# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data access layer."""

from pprint import pprint

from sqlalchemy.engine import Result
from sqlalchemy.future import select

from .db import Exam, Job, Record, async_session
from .models import BaseExam, BaseJob, RecordIn


async def exam_add(payload: BaseExam) -> Exam:
    """Create new exam.

    Parameters
    ----------
    payload
        Exam pydantic base model

    Returns
    -------
        Database orm model of created exam
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
    """Get exam by id.

    Parameters
    ----------
    exam_id
        Id of requested exam

    Returns
    -------
        Database orm model of exam or none
    """
    async with async_session() as session:
        exam: (Exam | None) = await session.get(Exam, exam_id)
    return exam


async def exam_get_all(patient_id: int) -> list[Exam]:
    """Get a list of all exams assigned to a certain patient.

    Parameters
    ----------
    patient_id
        Id of the parent patient entry, exams are assigned to

    Returns
    -------
        List of exam data base orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Exam).where(Exam.patient_id == patient_id))
        exams = list(result.scalars().all())
    return exams


async def exam_delete(exam_id: int) -> bool:
    """Delete exam by id.

    Parameters
    ----------
    exam_id
        Id of the exam to be deleted

    Returns
    -------
        Success of deletion
    """
    async with async_session() as session:
        if exam := await session.get(Exam, exam_id):
            await session.delete(exam)
            await session.commit()
            return True
        return False


async def update_exam(exam_id: int, payload: BaseExam) -> (Exam | None):
    """Update existing exam entry.

    Parameters
    ----------
    exam_id
        Id of the database entry to be updated

    payload
        Pydantic base exam model with data to be updated

    Returns
    -------
        Database orm model of updated exam
    """
    async with async_session() as session:
        if exam := await session.get(Exam, exam_id):
            exam.update(payload)
            await session.commit()
            await session.refresh(exam)
            return exam
        return None


async def add_job(payload: BaseJob) -> Job:
    """Add new job.

    Parameters
    ----------
    payload
        Job pydantic base model with data for job creation

    Returns
    -------
        Database orm model of created job
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
    """Get job by id.

    Parameters
    ----------
    job_id
        Id of the requested job

    Returns
    -------
        Database orm model with data of requested job
    """
    async with async_session() as session:
        job: (Job | None) = await session.get(Job, job_id)
    return job


async def get_all_jobs(exam_id: int) -> list[Job]:
    """Get a list of all jobs assigned to a certain exam.

    Parameters
    ----------
    exam_id
        Id of the parent exam entry, jobs are assigned to

    Returns
    -------
        List of job data base orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Job).where(Job.exam_id == exam_id))
        jobs = list(result.scalars().all())
    return jobs


async def delete_job(job_id: int) -> bool:
    """Delete a job by ID.

    Parameters
    ----------
    job_id
        ID of job to be deleted

    Returns
    -------
        Success of delete event
    """
    async with async_session() as session:
        if job := await session.get(Job, job_id):
            await session.delete(job)
            await session.commit()
            return True
        return False


async def update_job(job_id: int, payload: BaseJob) -> (Job | None):
    """Update existing job in database.

    Parameters
    ----------
    job_id
        Id of the job to be updateed
    payload
        Job pydantic base model with data to be updated

    Returns
    -------
        Job database orm model of updated job
    """
    async with async_session() as session:
        if job := await session.get(Job, job_id):
            job.update(payload)
            await session.commit()
            await session.refresh(job)
            return job
        return None


async def add_record(payload: RecordIn) -> Record:
    """Add new record to database.

    Parameters
    ----------
    payload
        Record pydantic input model

    Returns
    -------
        Database orm model of created record
    """
    new_record = Record(**payload.dict())
    async with async_session() as session:
        session.add(new_record)
        await session.commit()
        await session.refresh(new_record)
    return new_record


async def update_record(record_id: int, payload: dict) -> (Record | None):
    """Update existing record.

    Parameters
    ----------
    record_id
        Id of the record to be updated
    payload
        Dictionary with data to be updated

    Returns
    -------
        Database orm model of updated record
    """
    async with async_session() as session:
        record = await session.get(Record, record_id)
        if record:
            record.update(payload)
            await session.commit()
            await session.refresh(record)
            return record
        return None


async def get_record(record_id: int) -> (Record | None):
    """Get a record from database by id.

    Parameters
    ----------
    record_id
        Id of the requested record

    Returns
    -------
        Database orm model of requested record
    """
    async with async_session() as session:
        record: (Record | None) = await session.get(Record, record_id)
    return record


async def get_all_records(job_id: int) -> list[Record]:
    """Get a list of all records assigned to a certain job.

    Parameters
    ----------
    job_id
        Id of the parent job entry, records are assigned to

    Returns
    -------
        List of record data base orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Record).where(Record.job_id == job_id))
        records = list(result.scalars().all())
    return records


async def delete_record(record_id: int) -> bool:
    """Delete record by id.

    Parameters
    ----------
    record_id
        Id of the record to be deleted

    Returns
    -------
        Success of deletion
    """
    async with async_session() as session:
        if record := await session.get(Record, record_id):
            await session.delete(record)
            await session.commit()
            return True
        return False
