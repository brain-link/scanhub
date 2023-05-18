""" Exam api endpoints. """
from fastapi import APIRouter, HTTPException

from api.models import BaseExam, ExamOut, get_exam_out
from api.models import ProcedureOut, ProcedureIn, get_procedure_out
from api.models import JobOut, BaseJob, get_job_out
from api.models import RecordOut, RecordIn, get_record_out
from api import dal

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

router = APIRouter()

@router.get('/health/readiness', response_model={}, status_code=200)
async def readiness():
    return {'status': 'ok'}


# **************************************************
# Exams
# **************************************************

@router.post('/', response_model=ExamOut, status_code=201, tags=["exams"])
async def create_exam(payload: BaseExam):
    exam = await dal.add_exam(payload)
    if not exam:
        raise HTTPException(status_code=404, detail="Could not create exam")
    return await get_exam_out(exam)


@router.get('/{id}', response_model=ExamOut, status_code=200, tags=["exams"])
async def get_exam(id: int):
    exam = await dal.get_exam(id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(exam)


@router.get('/all/{patient_id}', response_model=list[ExamOut], status_code=200, tags=["exams"])
async def get_exam_list(patient_id: int):
    print("GET ALL EXAMS: ", patient_id)
    exams = await dal.get_all_exams(patient_id)
    if not exams:
        return []
        # raise HTTPException(status_code=404, detail="Exams not found")
    else:
        return [await get_exam_out(exam) for exam in exams]


@router.delete('/{id}', response_model={}, status_code=204, tags=["exams"])
async def delete_workflow(id: int):
    if not await dal.delete_exam(id):
        raise HTTPException(status_code=404, detail="Exam not found")
    

@router.put('/{id}', response_model=ExamOut, status_code=200, tags=["exams"])
async def update_workflow(id: int, payload: BaseExam):
    exam = await dal.update_exam(id, payload)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(exam)


# **************************************************
# Procedures
# **************************************************

@router.post('/procedure', response_model=ProcedureOut, status_code=201, tags=["procedures"])
async def create_procedure(payload: ProcedureIn):
    procedure = await dal.add_procedure(payload)
    if not procedure:
        raise HTTPException(status_code=404, detail="Could not create procedure")
    return await get_procedure_out(procedure)


@router.get('/procedure/{id}', response_model=ProcedureOut, status_code=200, tags=["procedures"])
async def get_procedure(id: int):
    procedure = await dal.get_procedure(id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return await get_procedure_out(procedure)


@router.get('/procedure/all/{exam_id}', response_model=list[ProcedureOut], status_code=200, tags=["procedures"])
async def get_procedure_list(exam_id: int):
    procedures = await dal.get_all_procedures(exam_id)
    if not procedures:
        return []
        # raise HTTPException(status_code=404, detail="Procedures not found")
    else:
        return [await get_procedure_out(procedure) for procedure in procedures]


@router.delete('/procedure/{id}', response_model={}, status_code=204, tags=["procedures"])
async def delete_procedure(id: int):
    if not await dal.delete_procedure(id):
        raise HTTPException(status_code=404, detail="Procedure not found")


@router.put('/procedure/{id}', response_model=ProcedureOut, status_code=200, tags=["procedures"])
async def update_procedure(id: int, payload: ProcedureIn):
    procedure = await dal.update_procedure(id, payload)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return await get_procedure_out(procedure)


# **************************************************
# Jobs
# **************************************************

@router.post('/job', response_model=JobOut, status_code=201, tags=["jobs"])
async def create_job(payload: BaseJob):
    job = await dal.add_job(payload)
    if not job:
        raise HTTPException(status_code=404, detail="Could not create job")
    # TODO: Query device, workflow if not None
    return await get_job_out(job)


@router.get('/job/{id}', response_model=JobOut, status_code=200, tags=["jobs"])
async def get_job(id: int):
    job = await dal.get_job(id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return await get_job_out(job)


@router.get('/job/all/{procedure_id}', response_model=list[JobOut], status_code=200, tags=["jobs"])
async def get_job_list(procedure_id: int):
    jobs = await dal.get_all_jobs(procedure_id)
    if not jobs:
        return []
        # raise HTTPException(status_code=404, detail="Jobs not found")
    else:
        return [await get_job_out(job) for job in jobs]


@router.delete('/job/{id}', response_model={}, status_code=204, tags=["jobs"])
async def delete_job(id: int):
    if not await dal.delete_job(id):
        raise HTTPException(status_code=404, detail="Job not found")
    

@router.put('/job/{id}', response_model=JobOut, status_code=200, tags=["jobs"])
async def update_job(id: int, payload: BaseJob):
    print("Updating job...")
    job = await dal.update_job(id, payload)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return await get_job_out(job)
 

# **************************************************
# Records
# **************************************************

@router.post('/record', response_model=RecordOut, status_code=201, tags=["records"])
async def create_record(payload: RecordIn):
    record = await dal.add_record(payload)
    if not record:
        raise HTTPException(status_code=404, detail="Could not create record")
    return await get_record_out(record)


@router.get('/record/{id}', response_model=RecordOut, status_code=200, tags=["records"])
async def get_record(id: int):
    record = await dal.get_record(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return await get_record_out(record)


@router.get('/record/all/{job_id}', response_model=list[RecordOut], status_code=200, tags=["records"])
async def get_record_list(job_id: int):
    records = await dal.get_all_records(job_id)
    if not records:
        return []
        # raise HTTPException(status_code=404, detail="Records not found")
    else:
        return [await get_record_out(record) for record in records]


@router.delete('/record/{id}', response_model={}, status_code=204, tags=["records"])
async def delete_record(_id: int):
    if not await dal.delete_record(_id):
        raise HTTPException(status_code=404, detail="Record not found")
