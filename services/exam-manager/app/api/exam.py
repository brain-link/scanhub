# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Exam API endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from . import dal
from .models import (
    BaseExam,
    BaseJob,
    ExamOut,
    JobOut,
    RecordIn,
    RecordOut,
    get_exam_out,
    get_job_out,
    get_record_out,
)

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

router = APIRouter()


@router.post("/", response_model=ExamOut, status_code=201, tags=["exams"])
async def exam_create(payload: BaseExam) -> ExamOut:
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
    if not (exam := await dal.exam_add(payload)):
        raise HTTPException(status_code=404, detail="Could not create exam")
    return await get_exam_out(data=exam)


@router.get("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
async def exam_get(exam_id: UUID | str) -> ExamOut:
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
    if not (exam := await dal.exam_get(_id)):
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(data=exam)


@router.get("/all/{patient_id}", response_model=list[ExamOut], status_code=200, tags=["exams"])
async def exam_get_all(patient_id: int) -> list[ExamOut]:
    """Get all exams of a patient endpoint.

    Parameters
    ----------
    patient_id
        Id of parent

    Returns
    -------
        List of exam pydantic output models
    """
    if not (exams := await dal.exam_get_all(patient_id)):
        # Don't raise exception here, list might be empty
        return []
    return [await get_exam_out(data=exam) for exam in exams]


@router.delete("/{exam_id}", response_model={}, status_code=204, tags=["exams"])
async def exam_delete(exam_id: UUID | str) -> None:
    """Delete exam by id.

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
    if not await dal.exam_delete(_id):
        raise HTTPException(status_code=404, detail="Exam not found")


@router.put("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
async def exam_update(exam_id: UUID | str, payload: BaseExam) -> ExamOut:
    """Update exam.

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
    if not (exam := await dal.update_exam(_id, payload)):
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(data=exam)


@router.post("/job", response_model=JobOut, status_code=201, tags=["jobs"])
async def job_create(payload: BaseJob) -> JobOut:
    """Create new job endpoint.

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
    if not (job := await dal.add_job(payload)):
        raise HTTPException(status_code=404, detail="Could not create job")
    return await get_job_out(data=job)


@router.get("/job/{job_id}", response_model=JobOut, status_code=200, tags=["jobs"])
async def job_get(job_id: UUID | str) -> JobOut:
    """Get job endpoint.

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
    if not (job := await dal.get_job(_id)):
        raise HTTPException(status_code=404, detail="Job not found")
    return await get_job_out(data=job)


@router.get(
    "/job/all/{exam_id}",
    response_model=list[JobOut],
    status_code=200,
    tags=["jobs"],
)
async def job_get_all(exam_id: UUID | str) -> list[JobOut]:
    """Get all jobs of a exam endpoint.

    Parameters
    ----------
    exam_id
        Id of parent exam

    Returns
    -------
        List of job pydantic output model
    """
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not (jobs := await dal.get_all_jobs(_id)):
        # Don't raise exception, list might be empty
        return []
    return [await get_job_out(data=job) for job in jobs]


@router.delete("/job/{job_id}", response_model={}, status_code=204, tags=["jobs"])
async def job_delete(job_id: UUID | str) -> None:
    """Delete job endpoint.

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
    if not await dal.delete_job(_id):
        raise HTTPException(status_code=404, detail="Job not found")


@router.put("/job/{job_id}", response_model=JobOut, status_code=200, tags=["jobs"])
async def job_update(job_id: UUID | str, payload: BaseJob) -> JobOut:
    """Update job endpoint.

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
    if not (job := await dal.update_job(_id, payload)):
        raise HTTPException(status_code=404, detail="Job not found")
    return await get_job_out(data=job)


@router.post("/record", response_model=RecordOut, status_code=201, tags=["records"])
async def record_create(payload: RecordIn) -> RecordOut:
    """Create record endpoint.

    Parameters
    ----------
    payload
        Record pydantic input model

    Returns
    -------
        Record pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    if not (record := await dal.add_record(payload)):
        raise HTTPException(status_code=404, detail="Could not create record")
    return await get_record_out(data=record)


@router.put("/record/{record_id}/", response_model=RecordOut, status_code=200, tags=["records"])
async def update_record(record_id: UUID | str, payload: RecordIn):
    """Update existing record.

    Parameters
    ----------
    record_id
        Id of the record to be updated
    payload
        Record pydantic input model

    Returns
    -------
        Record pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(record_id) if not isinstance(record_id, UUID) else record_id
    record = await dal.update_record(_id, payload)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return await get_record_out(record)


@router.get("/record/{record_id}", response_model=RecordOut, status_code=200, tags=["records"])
async def record_get(record_id: UUID | str) -> RecordOut:
    """Get single record endpoint.

    Parameters
    ----------
    record_id
        Id of the record to return

    Returns
    -------
        Record pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(record_id) if not isinstance(record_id, UUID) else record_id
    if not (record := await dal.get_record(_id)):
        raise HTTPException(status_code=404, detail="Record not found")
    return await get_record_out(data=record)


@router.get(
    "/record/all/{job_id}",
    response_model=list[RecordOut],
    status_code=200,
    tags=["records"],
)
async def record_get_all(job_id: UUID | str) -> list[RecordOut]:
    """Get all records of a job endpoint.

    Parameters
    ----------
    job_id
        Id of parental job

    Returns
    -------
        List of record pydantic output model
    """
    _id = UUID(job_id) if not isinstance(job_id, UUID) else job_id
    if not (records := await dal.get_all_records(_id)):
        # Don't raise exception here, list might be empty.
        return []
    return [await get_record_out(data=record) for record in records]


@router.delete("/record/{record_id}", response_model={}, status_code=204, tags=["records"])
async def record_delete(record_id: UUID | str) -> None:
    """Delete record endpoint.

    Parameters
    ----------
    record_id
        Id of the record to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    _id = UUID(record_id) if not isinstance(record_id, UUID) else record_id
    if not await dal.delete_record(_id):
        raise HTTPException(status_code=404, detail="Record not found")
