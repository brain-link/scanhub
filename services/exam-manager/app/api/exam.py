from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from typing import Any

from api.models import BaseExam, ExamOut
from api.models import BaseProcedure, ProcedureIn, ProcedureOut
# from api.models import BaseProcedure, ProcedureOut, ProcedureIn
# from api.models import BaseRecord, RecordOut, RecordIn
from api import dal


exam = APIRouter()



@exam.get('/exam/{id}', response_model=ExamOut, tags=["exam"])
async def get_exam(id: int) -> Any:
    exam = await dal.get_exam(id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@exam.get('/procedure/{id}', response_model=ProcedureOut)
async def get_procedure(id: int) -> Any:
    procedure = await dal.get_procedure(id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return procedure

# @exam.get('/record/{id}', response_model=RecordOut)
# async def get_record(id: int) -> Any:
#     record = await dal.get_record(id)
#     if not record:
#         raise HTTPException(status_code=404, detail="Record not found")
#     return record

@exam.get('/exams/{patientID}', response_model=list[ExamOut], tags=["exam"])
async def get_exams(patient_id: str) -> Any:
    exams = await dal.get_all_exams(patient_id)
    if not exams:
        raise HTTPException(status_code=404, detail="Exams not found")
    return exams


@exam.get('/procedures/{examID}', response_model=list[ProcedureOut])
async def get_procedures(examID: int) -> Any:
    procedures = await dal.get_procedures(examID)
    if not procedures:
        raise HTTPException(status_code=404, detail="Procedures not found")
    return procedures

# @exam.get('/records/{procedureID}', response_model=list[RecordOut])
# async def get_records(procedureID: int) -> Any:
#     records = await dal.get_records(procedureID)
#     if not records:
#         raise HTTPException(status_code=404, detail="Records not found")
#     return records

@exam.post('/exam', response_model=None, status_code=201, tags=["exam"])
async def create_exam(payload: BaseExam) -> Any:
    return await dal.add_exam(payload)

@exam.post('/procedure', response_model=ProcedureOut, status_code=201)
async def create_procedure(payload: ProcedureIn) -> Any:
    print(payload)
    return await dal.add_procedure(payload)

# @exam.post('/record', response_model=RecordOut, status_code=201)
# async def create_record(payload: RecordIn) -> Any:
#     # record_id = await dal.add_record(payload)

#     # response = {
#     #     'id': record_id,
#     #     **payload.dict()
#     # }

#     response = ExamOut( 
#         id=1
#     )

#     return response

# @exam.delete('/exam/{id}', response_model=ExamOut, tags=["exam"])
# async def delete_exam(id: int) -> Any:
#     response = await dal.delete_exam(id)
#     if not response:
#         raise HTTPException(status_code=404, detail="Exam not found")
#     return response

# @exam.delete('/procedure/{id}', response_model=ExamOut)
# async def delete_procedure(id: int) -> Any:
#     procedure = await dal.get_procedure(id)
#     if not procedure:
#         raise HTTPException(status_code=404, detail="Procedure not found")
#     return procedure

# @exam.delete('/record/{id}', response_model=ExamOut)
# async def delete_record(id: int):
#     record = await dal.get_record(id)
#     if not record:
#         raise HTTPException(status_code=404, detail="Record not found")
#     return record

# @exam.put('/exam/{id}', response_model=ExamOut, tags=["exam"])
# async def update_exam(id: int, payload: BaseExam) -> Any:
#     exam = await dal.update_exam(id, payload)
#     if not exam:
#         raise HTTPException(status_code=404, detail="Exam not found")
#     return exam
