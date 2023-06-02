# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Exam API endpoints."""

from api import dal
from api.models import (BaseExam, BaseJob, ExamOut, JobOut, ProcedureIn,
                        ProcedureOut, RecordIn, RecordOut, get_exam_out,
                        get_job_out, get_procedure_out, get_record_out)
from fastapi import APIRouter, HTTPException

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

router = APIRouter()


@router.post('/', response_model=ExamOut, status_code=201, tags=["exams"])
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


@router.get('/{exam_id}', response_model=ExamOut, status_code=200, tags=["exams"])
async def exam_get(exam_id: int) -> ExamOut:
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
    if not (exam := await dal.exam_get(exam_id)):
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(data=exam)


@router.get('/all/{patient_id}', response_model=list[ExamOut], status_code=200, tags=["exams"])
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


@router.delete('/{exam_id}', response_model={}, status_code=204, tags=["exams"])
async def exam_delete(exam_id: int) -> None:
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
    if not await dal.exam_delete(exam_id):
        raise HTTPException(status_code=404, detail="Exam not found")


@router.put('/{exam_id}', response_model=ExamOut, status_code=200, tags=["exams"])
async def exam_update(exam_id: int, payload: BaseExam) -> ExamOut:
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
    if not (exam := await dal.update_exam(exam_id, payload)):
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(data=exam)


@router.post('/procedure', response_model=ProcedureOut, status_code=201, tags=["procedures"])
async def procedure_create(payload: ProcedureIn) -> ProcedureOut:
    """Procedure post endpoint.

    Parameters
    ----------
    payload
        Pydantic input model

    Returns
    -------
        Pydantic output model

    Raises
    ------
    HTTPException
        404: Creation not succesful
    """
    if not (procedure := await dal.procedure_add(payload)):
        raise HTTPException(status_code=404, detail="Could not create procedure")
    return await get_procedure_out(data=procedure)


@router.get('/procedure/{procedure_id}', response_model=ProcedureOut, status_code=200, tags=["procedures"])
async def procedure_get(procedure_id: int) -> ProcedureOut:
    """Procedure get endpoint.

    Parameters
    ----------
    procedure_id
        Id of entry to return

    Returns
    -------
        Pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not (procedure := await dal.procedure_get(procedure_id)):
        raise HTTPException(status_code=404, detail="Procedure not found")
    return await get_procedure_out(data=procedure)


@router.get('/procedure/all/{exam_id}', response_model=list[ProcedureOut], status_code=200, tags=["procedures"])
async def procedure_get_all(exam_id: int) -> list[ProcedureOut]:
    """Get all procedures of a parent endpoint.

    Parameters
    ----------
    exam_id
        Id of the parent object

    Returns
    -------
        List of pydantic output models
    """
    if not (procedures := await dal.procedure_get_all(exam_id)):
        # Don't raise exception, list might be empty
        return []
    return [await get_procedure_out(data=procedure) for procedure in procedures]


@router.delete('/procedure/{procedure_id}', response_model={}, status_code=204, tags=["procedures"])
async def procedure_delete(procedure_id: int) -> None:
    """Delete procedure endpoint.

    Parameters
    ----------
    procedure_id
        Id of entry to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not await dal.procedure_delete(procedure_id):
        raise HTTPException(status_code=404, detail="Procedure not found")


@router.put('/procedure/{procedure_id}', response_model=ProcedureOut, status_code=200, tags=["procedures"])
async def proceedure_update(procedure_id: int, payload: ProcedureIn) -> ProcedureOut:
    """Update procedure endpoint.

    Parameters
    ----------
    procedure_id
        Id of procedure to be updated
    payload
        Pydantic input model

    Returns
    -------
        Pydantic output model

    Raises
    ------
    HTTPException
        404: Entry not found
    """
    if not (procedure := await dal.procedure_update(procedure_id, payload)):
        raise HTTPException(status_code=404, detail="Procedure not found")
    return await get_procedure_out(data=procedure)


@router.post('/job', response_model=JobOut, status_code=201, tags=["jobs"])
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
    # TODO: Query device, workflow if not None
    return await get_job_out(data=job)


@router.get('/job/{job_id}', response_model=JobOut, status_code=200, tags=["jobs"])
async def job_get(job_id: int) -> JobOut:
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
    if not (job := await dal.get_job(job_id)):
        raise HTTPException(status_code=404, detail="Job not found")
    return await get_job_out(data=job)


@router.get('/job/all/{procedure_id}', response_model=list[JobOut], status_code=200, tags=["jobs"])
async def job_get_all(procedure_id: int) -> list[JobOut]:
    """Get all jobs of a procedure endpoint.

    Parameters
    ----------
    procedure_id
        Id of parent procedure

    Returns
    -------
        List of job pydantic output model
    """
    if not (jobs := await dal.get_all_jobs(procedure_id)):
        # Don't raise exception, list might be empty
        return []
    return [await get_job_out(data=job) for job in jobs]


@router.delete('/job/{job_id}', response_model={}, status_code=204, tags=["jobs"])
async def job_delete(job_id: int) -> None:
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
    if not await dal.delete_job(job_id):
        raise HTTPException(status_code=404, detail="Job not found")


@router.put('/job/{job_id}', response_model=JobOut, status_code=200, tags=["jobs"])
async def job_update(job_id: int, payload: BaseJob) -> JobOut:
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
    if not (job := await dal.update_job(job_id, payload)):
        raise HTTPException(status_code=404, detail="Job not found")
    return await get_job_out(data=job)


@router.post('/record', response_model=RecordOut, status_code=201, tags=["records"])
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


@router.get('/record/{record_id}', response_model=RecordOut, status_code=200, tags=["records"])
async def record_get(record_id: int) -> RecordOut:
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
    if not (record := await dal.get_record(record_id)):
        raise HTTPException(status_code=404, detail="Record not found")
    return await get_record_out(data=record)


@router.get('/record/all/{job_id}', response_model=list[RecordOut], status_code=200, tags=["records"])
async def record_get_all(job_id: int) -> list[RecordOut]:
    """Get all records of a job endpoint.

    Parameters
    ----------
    job_id
        Id of parental job

    Returns
    -------
        List of record pydantic output model
    """
    if not (records := await dal.get_all_records(job_id)):
        # Don't raise exception here, list might be empty.
        return []
    return [await get_record_out(data=record) for record in records]


@router.delete('/record/{record_id}', response_model={}, status_code=204, tags=["records"])
async def record_delete(record_id: int) -> None:
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
    if not await dal.delete_record(record_id):
        raise HTTPException(status_code=404, detail="Record not found")
