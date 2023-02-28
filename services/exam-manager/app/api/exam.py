from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from typing import List
import os

import uuid

import json
from pydantic import BaseModel, StrictStr

from api.models import ExamOut, ExamIn, ExamUpdate
from api import db_manager


exam = APIRouter()

### NEW API

@exam.get('/exam/{id}', response_model=ExamOut)
async def get_exam(id: int):
    exam = await db_manager.get_exam(id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@exam.get('/procedure/{id}', response_model=ExamOut)
async def get_procedure(id: int):
    procedure = await db_manager.get_procedure(id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return procedure

@exam.get('/record/{id}', response_model=ExamOut)
async def get_record(id: int):
    record = await db_manager.get_record(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@exam.get('/exams/{patientID}', response_model=ExamOut)
async def get_exams(patientID: int):
    exams = await db_manager.get_exams(patientID)
    if not exams:
        raise HTTPException(status_code=404, detail="Exams not found")
    return exams

@exam.get('/procedures/{examID}', response_model=ExamOut)
async def get_procedures(examID: int):
    procedures = await db_manager.get_procedures(examID)
    if not procedures:
        raise HTTPException(status_code=404, detail="Procedures not found")
    return procedures

@exam.get('/records/{procedureID}', response_model=ExamOut)
async def get_records(procedureID: int):
    records = await db_manager.get_records(procedureID)
    if not records:
        raise HTTPException(status_code=404, detail="Records not found")
    return records

@exam.post('/exam', response_model=ExamOut, status_code=201)
async def create_exam(payload: ExamIn):
    # exam_id = await db_manager.add_exam(payload)

    # response = {
    #     'id': exam_id,
    #     **payload.dict()
    # }

    response = ExamOut( 
        id=1
    )

    return response

@exam.post('/procedure', response_model=ExamOut, status_code=201)
async def create_procedure(payload: ExamIn):
    # procedure_id = await db_manager.add_procedure(payload)

    # response = {
    #     'id': procedure_id,
    #     **payload.dict()
    # }

    response = ExamOut( 
        id=1
    )

    return response

@exam.post('/record', response_model=ExamOut, status_code=201)
async def create_record(payload: ExamIn):
    # record_id = await db_manager.add_record(payload)

    # response = {
    #     'id': record_id,
    #     **payload.dict()
    # }

    response = ExamOut( 
        id=1
    )

    return response

@exam.delete('/exam/{id}', response_model=ExamOut)
async def delete_exam(id: int):
    exam = await db_manager.get_exam(id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@exam.delete('/procedure/{id}', response_model=ExamOut)
async def delete_procedure(id: int):
    procedure = await db_manager.get_procedure(id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return procedure

@exam.delete('/record/{id}', response_model=ExamOut)
async def delete_record(id: int):
    record = await db_manager.get_record(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
