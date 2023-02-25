from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from typing import List
import os

import uuid

import json
from pydantic import BaseModel, StrictStr

from app.api.models import ExamOut, ExamIn, ExamUpdate
from app.api import db_manager


exam = APIRouter()

@exam.post('/exam', response_model=ExamOut, status_code=201)
async def create_exam(payload: ExamIn):
    exam_id = await db_manager.add_exam(payload)

    response = {
        'id': exam_id,
        **payload.dict()
    }

    return response
