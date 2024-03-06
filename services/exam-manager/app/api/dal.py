# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data acess layer (DAL) between fastapi endpoint and sql database."""

from pprint import pprint
from uuid import UUID

from scanhub_libraries.models import BaseExam, BaseJob, BaseTask
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from .db import (
    Exam,
    ExamDefinitions,
    ExamTemplates,
    Job,
    JobDefinitions,
    JobTemplates,
    Task,
    TaskDefinitions,
    TaskTemplates,
    async_session,
)

# ----- Exam data access layer

async def add_exam(payload: BaseExam, is_template: bool = False) -> Exam:
    """Create new exam.

    Parameters
    ----------
    payload
        Exam pydantic base model

    Returns
    -------
        Database orm model of created exam
    """
    new_exam = ExamTemplates(**payload.dict()) if is_template else ExamDefinitions(**payload.dict())
    async with async_session() as session:
        session.add(new_exam)
        await session.commit()
        await session.refresh(new_exam)
    # debug
    print("***** NEW EXAM *****")
    pprint(new_exam.__dict__)
    return new_exam


async def get_exam(exam_id: UUID, is_template: bool = False) -> (Exam | None):
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
        exam = await session.get(ExamTemplates if is_template else ExamDefinitions, exam_id)
    return exam


async def get_all_exams(patient_id: int, is_template: bool = False) -> list[Exam]:
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
        if is_template:
            result: Result = await session.execute(select(ExamTemplates).where(ExamTemplates.patient_id == patient_id))
        else:
            result: Result = await session.execute(select(ExamDefinitions).where(ExamDefinitions.patient_id == patient_id))
        exams = list(result.scalars().all())
    return exams


async def delete_exam(exam_id: UUID, is_template: bool = False) -> bool:
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
        if exam := await session.get(ExamTemplates if is_template else ExamDefinitions, exam_id):
            await session.delete(exam)
            await session.commit()
            return True
        return False


async def update_exam(exam_id: UUID, payload: BaseExam, is_template: bool = False) -> (Exam | None):
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
        if exam := await session.get(ExamTemplates if is_template else ExamDefinitions, exam_id):
            exam.update(payload)
            await session.commit()
            await session.refresh(exam)
            return exam
        return None


# ----- Job data access layer

async def add_job(payload: BaseJob, is_template: bool = False) -> Job:
    """Add new job.

    Parameters
    ----------
    payload
        Job pydantic base model with data for job creation

    Returns
    -------
        Database orm model of created job
    """
    new_job = JobTemplates(**payload.dict()) if is_template else JobDefinitions(**payload.dict())
    async with async_session() as session:
        session.add(new_job)
        await session.commit()
        await session.refresh(new_job)
    # Debugging
    print("***** NEW JOB *****")
    pprint(new_job.__dict__)
    return new_job


async def get_job(job_id: UUID, is_template: bool = False) -> (Job | None):
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
        job = await session.get(JobTemplates if is_template else JobDefinitions, job_id)
    return job


async def get_all_jobs(exam_id: UUID, is_template: bool = False) -> list[Job]:
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
        if is_template:
            result: Result = await session.execute(select(JobTemplates).where(JobTemplates.exam_id == exam_id))
        else:
            result: Result = await session.execute(select(JobDefinitions).where(JobDefinitions.exam_id == exam_id))
        jobs = list(result.scalars().all())
    return jobs


async def delete_job(job_id: UUID, is_template: bool = False) -> bool:
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
        if job := await session.get(JobTemplates if is_template else JobDefinitions, job_id):
            await session.delete(job)
            await session.commit()
            return True
        return False


async def update_job(job_id: UUID, payload: BaseJob, is_template: bool = False) -> (Job | None):
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
        if job := await session.get(JobTemplates if is_template else JobDefinitions, job_id):
            job.update(payload)
            await session.commit()
            await session.refresh(job)
            return job
        return None


# ----- Task data access layer

async def add_task(payload: BaseTask, is_template: bool = False) -> Task:
    """Add new task to database.

    Parameters
    ----------
    payload
        Task pydantic base model

    Returns
    -------
        Database orm model of created task
    """
    new_task = TaskTemplates(**payload.dict()) if is_template else TaskDefinitions(**payload.dict())
    async with async_session() as session:
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
    return new_task


async def get_task(task_id: UUID, is_template: bool = False) -> (Task | None):
    """Get task by id.

    Parameters
    ----------
    task_id
        Id of the requested task

    Returns
    -------
        Database orm model with data of requested task
    """
    async with async_session() as session:
        task = await session.get(TaskTemplates if is_template else TaskDefinitions, task_id)
    return task


async def get_all_tasks(job_id: UUID, is_template: bool = False) -> list[Task]:
    """Get a list of all tasks assigned to a certain job.

    Parameters
    ----------
    job_id
        Id of the parent job entry, tasks are assigned to

    Returns
    -------
        List of task data base orm models
    """
    async with async_session() as session:
        if is_template:
            result: Result = await session.execute(select(TaskTemplates).where(TaskTemplates.job_id == job_id))
        else:
            result: Result = await session.execute(select(TaskDefinitions).where(TaskDefinitions.job_id == job_id))
        tasks = list(result.scalars().all())
    return tasks


async def delete_task(task_id: UUID, is_template: bool = False) -> bool:
    """Delete task by id.

    Parameters
    ----------
    task_id
        Id of the task to be deleted

    Returns
    -------
        Success of deletion
    """
    async with async_session() as session:
        if task := await session.get(TaskTemplates if is_template else TaskDefinitions, task_id):
            await session.delete(task)
            await session.commit()
            return True
        return False


async def update_task(task_id: UUID, payload: BaseTask, is_template: bool = False) -> (Task | None):
    """Update existing task in database.

    Parameters
    ----------
    task_id
        Id of the task to be updateed
    payload
        Task pydantic base model with data to be updated

    Returns
    -------
        Database orm model of updated task
    """
    async with async_session() as session:
        if task := await session.get(TaskTemplates if is_template else TaskDefinitions, task_id):
            task.update(payload)
            await session.commit()
            await session.refresh(task)
            return task
        return None
