from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from api.models import BaseExam, ExamOut, get_exam_out
from api.models import ProcedureOut, ProcedureIn, get_procedure_out
from api.models import RecordOut, RecordIn, get_record_out
from api import dal

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

exam = APIRouter()


# **************************************************
# RECORDS
# **************************************************

@exam.post('/exam/', response_model=ExamOut, status_code=201, tags=["exams"])
async def create_exam(payload: BaseExam):
    exam = dal.add_exam(payload)
    if not exam:
        raise HTTPException(status_code=404, detail="Could not create exam")
    return await get_exam_out(exam)


@exam.get('/exam/{id}', response_model=ExamOut, status_code=200, tags=["exams"])
async def get_exam(id: int):
    exam = await dal.get_exam(id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(exam)


@exam.get('/exams/{patientID}', response_model=list[ExamOut], status_code=200, tags=["exams"])
async def get_exam_list(patient_id: str):
    exams = await dal.get_all_exams(patient_id)
    if not exams:
        raise HTTPException(status_code=404, detail="Exams not found")
    return [await get_exam_out(exam) for exam in exams]


@exam.delete('/exam/{id}/', response_model={}, status_code=204, tags=["exams"])
async def delete_workflow(id: int):
    if not await dal.delete_exam(id):
        raise HTTPException(status_code=404, detail="Exam not found")
    

@exam.put('/exam/{id}/', response_model=ExamOut, status_code=200, tags=["exams"])
async def update_workflow(id: int, payload: BaseExam):
    exam = await dal.update_exam(id, payload)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out(exam)


# **************************************************
# Procedures
# **************************************************

@exam.post('/procedure/', response_model=ProcedureOut, status_code=201, tags=["procedures"])
async def create_procedure(payload: ProcedureIn):
    procedure = dal.add_procedure(payload)
    if not procedure:
        raise HTTPException(status_code=404, detail="Could not create procedure")
    return await get_procedure_out(procedure)


@exam.get('/procedure/{id}/', response_model=ProcedureOut, status_code=200, tags=["procedures"])
async def get_procedure(id: int):
    procedure = await dal.get_procedure(id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return await get_procedure_out(procedure)


@exam.get('/procedures/{exam_id}/', response_model=list[ProcedureOut], status_code=200, tags=["procedures"])
async def get_procedure_list(exam_id: int):
    procedures = await dal.get_procedures(exam_id)
    if not procedures:
        raise HTTPException(status_code=404, detail="Procedures not found")
    return [await get_exam_out(procedure) for procedure in procedures]


@exam.delete('/procedure/{id}', response_model={}, status_code=204, tags=["procedures"])
async def delete_procedure(id: int):
    if not await dal.delete_procedure(id):
        raise HTTPException(status_code=404, detail="Procedure not found")


@exam.por('/procedure/{id}', response_model=ProcedureOut, status_code=200, tags=["procedures"])
async def update_procedure(id: int, payload: ProcedureIn):
    procedure = await dal.update_procedure(payload)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return await get_procedure_out(procedure)


# **************************************************
# Records
# **************************************************

@exam.post('/record/{id}', response_model=RecordOut, status_code=201, tags=["records"])
async def create_record(payload: RecordIn):
    record = await dal.add_record(payload)
    if not record:
        raise HTTPException(status_code=404, detail="Could not create record")
    return await get_record_out(record)


@exam.get('/record/{id}/', response_model=RecordOut, status_code=200, tags=["records"])
async def get_record(id: int):
    record = await dal.get_record(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return await get_record_out(record)


@exam.get('/records/{procedure_id}/', response_model=list[RecordOut], status_code=200, tags=["records"])
async def get_record_list(procedure_id: int):
    records = await dal.get_all_records(procedure_id)
    if not records:
        raise HTTPException(status_code=404, detail="Records not found")
    return [await get_record_out(record) for record in records]


@exam.delete('/record/{id}/', response_model={}, status_code=204, tags=["records"])
async def delete_record(id: int):
    if not dal.delete_record(id):
        raise HTTPException(status_code=404, detail="Record not found")
    

@exam.put('/record/{id}/', response_model=RecordOut, status_code=200, tags=["records"])
async def update_record(id: int, payload: RecordIn):
    record = await dal.update_record(id, payload)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return await get_record_out(record)
 