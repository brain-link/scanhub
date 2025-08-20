# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data acess layer (DAL) between fastapi endpoint and sql database."""

from pprint import pprint
from uuid import UUID

from scanhub_libraries.models import BaseExam
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from app.db.postgres import (
    Exam,
    async_session,
)

# ----- Exam data access layer


async def add_exam_data(payload: BaseExam, creator: str) -> Exam:
    """Create new exam.

    Parameters
    ----------
    payload
        Exam pydantic base model
    creator
        The username/id of the user who creats this exam

    Returns
    -------
        Database orm model of created exam
    """
    new_exam = Exam(**payload.model_dump(), creator=creator)
    async with async_session() as session:
        session.add(new_exam)
        await session.commit()
        await session.refresh(new_exam)
    # debug
    print("***** NEW EXAM *****")
    pprint(new_exam.__dict__)
    return new_exam


async def get_exam_data(exam_id: UUID) -> Exam | None:
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
        exam = await session.get(Exam, exam_id)
    return exam


async def get_all_exam_data(patient_id: UUID) -> list[Exam]:
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


async def get_all_exam_template_data() -> list[Exam]:
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
        result: Result = await session.execute(select(Exam).where(Exam.is_template))
        exams = list(result.scalars().all())
    return exams


async def delete_exam_data(exam_id: UUID) -> bool:
    """Delete exam by id. Also deletes associated workflows and tasks.

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
            for workflow in exam.workflows:
                for task in workflow.tasks:
                    await session.delete(task)
                await session.delete(workflow)
            await session.delete(exam)
            await session.commit()
            return True
        return False


async def update_exam_data(exam_id: UUID, payload: BaseExam) -> Exam | None:
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
