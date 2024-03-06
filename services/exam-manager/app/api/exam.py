# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of exam API endpoints accessible through swagger UI."""

from uuid import UUID

from fastapi import APIRouter, HTTPException
from scanhub_libraries.models import BaseExam, BaseJob, BaseTask, ExamOut, JobOut, TaskOut

from . import dal
from .db import Exam, Job

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

router = APIRouter()


# Helper methods for jobs and exam, require recursive model translation
async def get_job_out(data: Job) -> JobOut:
    """Transform db model to pydantic model.

    Parameters
    ----------
    data
        Job db model

    Returns
    -------
        Job pydantic model
    """
    job = data.__dict__
    job["tasks"] = [TaskOut(**task.__dict__) for task in data.tasks]
    return JobOut(**job)


async def get_exam_out(data: Exam) -> ExamOut:
    """Transform db model to pydantic model.

    Parameters
    ----------
    data
        Exam db model

    Returns
    -------
        Exam pydantic model
    """
    exam = data.__dict__
    exam["jobs"] = [await get_job_out(job) for job in data.jobs]
    return ExamOut(**exam)


# ----- Exam API endpoints
@router.post("/", response_model=ExamOut, status_code=201, tags=["exams"])
async def create_exam(payload: BaseExam, is_template: bool = False) -> ExamOut:
    """Create exam endpoint.

    Parameters
    ----------
    payload
        Exam pydantic input model.

    Returns
    -------
        Exam pydantic output moddel.

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    if not (exam := await dal.add_exam(payload=payload, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Could not create exam")
    return await get_exam_out(data=exam)


@router.get("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
async def get_exam(exam_id: UUID | str, is_template: bool) -> ExamOut:
    """Get exam endpoint.

    Parameters
    ----------
    exam_id
        Id of requested exam entry

    Returns
    -------
        Exam pydantic output model.

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not (exam := await dal.get_exam(exam_id=_id, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(data=exam)


@router.get("/all/{patient_id}", response_model=list[ExamOut], status_code=200, tags=["exams"])
async def get_all_exams(patient_id: int, is_template: bool) -> list[ExamOut]:
    """Get all exams of a certain patient.

    Parameters
    ----------
    patient_id
        Id of parent

    Returns
    -------
        List of exam pydantic output models
    """
    if not (exams := await dal.get_all_exams(patient_id=patient_id, is_template=is_template)):
        # Don't raise exception here, list might be empty
        return []
    result = [await get_exam_out(data=exam) for exam in exams]
    print("Exam list: ", result)
    return result


@router.delete("/{exam_id}", response_model={}, status_code=204, tags=["exams"])
async def exam_delete(exam_id: UUID | str, is_template: bool) -> None:
    """Delete an existing exam by id.

    Parameters
    ----------
    exam_id
        Id of the exam to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not await dal.delete_exam(exam_id=_id, is_template=is_template):
        raise HTTPException(status_code=404, detail="Exam not found")


@router.put("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
async def exam_update(exam_id: UUID | str, payload: BaseExam, is_template: bool) -> ExamOut:
    """Update an existing exam.

    Parameters
    ----------
    exam_id
        Id of the exam to be updated
    payload
        Exam pydantic input model

    Returns
    -------
        Exam pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not (exam := await dal.update_exam(exam_id=_id, payload=payload, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(data=exam)


# ----- Job API endpoints
@router.post("/job", response_model=JobOut, status_code=201, tags=["jobs"])
async def job_create(payload: BaseJob, is_template: bool) -> JobOut:
    """Create new job.

    Parameters
    ----------
    payload
        Job pydantic input model

    Returns
    -------
        Job pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print("Payload: ", payload.__dict__)
    if not (job := await dal.add_job(payload=payload, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Could not create job")
    print("New job: ", job)
    return await get_job_out(data=job)


@router.get("/job/{job_id}", response_model=JobOut, status_code=200, tags=["jobs"])
async def job_get(job_id: UUID | str, is_template: bool) -> JobOut:
    """Get a job.

    Parameters
    ----------
    job_id
        Id of the job to be returned

    Returns
    -------
        Job pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(job_id) if not isinstance(job_id, UUID) else job_id
    if not (job := await dal.get_job(job_id=_id, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Job not found")
    return await get_job_out(data=job)


@router.get(
    "/job/all/{exam_id}",
    response_model=list[JobOut],
    status_code=200,
    tags=["jobs"],
)
async def job_get_all(exam_id: UUID | str, is_template: bool) -> list[JobOut]:
    """Get all existing jobs of a certain exam.

    Parameters
    ----------
    exam_id
        Id of parent exam

    Returns
    -------
        List of job pydantic output model
    """
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not (jobs := await dal.get_all_jobs(exam_id=_id, is_template=is_template)):
        # Don't raise exception, list might be empty
        return []
    return [await get_job_out(data=job) for job in jobs]


@router.delete("/job/{job_id}", response_model={}, status_code=204, tags=["jobs"])
async def job_delete(job_id: UUID | str, is_template: bool) -> None:
    """Delete an existing job.

    Parameters
    ----------
    job_id
        Id of the job to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(job_id) if not isinstance(job_id, UUID) else job_id
    if not await dal.delete_job(job_id=_id, is_template=is_template):
        raise HTTPException(status_code=404, detail="Job not found")


@router.put("/job/{job_id}", response_model=JobOut, status_code=200, tags=["jobs"])
async def job_update(job_id: UUID | str, payload: BaseJob, is_template: bool) -> JobOut:
    """Update an existing job.

    Parameters
    ----------
    job_id
        Id of the job to be updated
    payload
        Job pydantic indput model

    Returns
    -------
        Job pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(job_id) if not isinstance(job_id, UUID) else job_id
    if not (job := await dal.update_job(job_id=_id, payload=payload, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Job not found")
    return await get_job_out(data=job)


# ----- Task API endpoints
@router.post("/task", response_model=TaskOut, status_code=201, tags=["tasks"])
async def task_create(payload: BaseTask, is_template: bool) -> TaskOut:
    """Create a new task.

    Parameters
    ----------
    payload
        Task pydantic input model

    Returns
    -------
        Task pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    if not (task := await dal.add_task(payload=payload, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Could not create task")
    result = TaskOut(**task.__dict__)
    print("Task created: ", result)
    return result


@router.get("/task/{task_id}", response_model=TaskOut, status_code=200, tags=["tasks"])
async def task_get(task_id: UUID | str, is_template: bool) -> TaskOut:
    """Get an existing task.

    Parameters
    ----------
    task_id
        Id of the task to be returned

    Returns
    -------
        Task pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not (task := await dal.get_task(task_id=_id, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut(**task.__dict__)


@router.get(
    "/task/all/{job_id}",
    response_model=list[TaskOut],
    status_code=200,
    tags=["tasks"],
)
async def task_get_all(job_id: UUID | str, is_template: bool) -> list[TaskOut]:
    """Get all existing tasks of a certain job.

    Parameters
    ----------
    job_id
        Id of parental job

    Returns
    -------
        List of task pydantic output model
    """
    _id = UUID(job_id) if not isinstance(job_id, UUID) else job_id
    if not (tasks := await dal.get_all_tasks(job_id=_id, is_template=is_template)):
        # Don't raise exception here, list might be empty.
        return []
    result = [TaskOut(**task.__dict__) for task in tasks]
    print("List of tasks: ", result)
    return result


@router.delete("/task/{task_id}", response_model={}, status_code=204, tags=["tasks"])
async def task_delete(task_id: UUID | str, is_template: bool) -> None:
    """Delete an existing task.

    Parameters
    ----------
    task_id
        Id of the task to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not await dal.delete_task(task_id=_id, is_template=is_template):
        raise HTTPException(status_code=404, detail="Task not found")


@router.put("/task/{task_id}", response_model=TaskOut, status_code=200, tags=["tasks"])
async def task_update(task_id: UUID | str, payload: BaseTask, is_template: bool) -> TaskOut:
    """Update an existing task.

    Parameters
    ----------
    task_id
        Id of the job to be updated
    payload
        Task pydantic base model

    Returns
    -------
        Task pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not (task := await dal.update_task(task_id=_id, payload=payload, is_template=is_template)):
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut(**task.__dict__)
