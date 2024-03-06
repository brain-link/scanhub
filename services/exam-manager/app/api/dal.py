# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data acess layer (DAL) between fastapi endpoint and sql database."""

from pprint import pprint
from uuid import UUID

from scanhub_libraries.models import BaseExam, BaseWorkflow, BaseTask
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from .db import (
    Exam,
    ExamDefinitions,
    ExamTemplates,
    Workflow,
    WorkflowDefinitions,
    WorkflowTemplates,
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


# ----- Workflow data access layer

async def add_workflow(payload: BaseWorkflow, is_template: bool = False) -> Workflow:
    """Add new workflow.

    Parameters
    ----------
    payload
        Workflow pydantic base model with data for workflow creation

    Returns
    -------
        Database orm model of created workflow
    """
    new_workflow = WorkflowTemplates(**payload.dict()) if is_template else WorkflowDefinitions(**payload.dict())
    async with async_session() as session:
        session.add(new_workflow)
        await session.commit()
        await session.refresh(new_workflow)
    # Debugging
    print("***** NEW JOB *****")
    pprint(new_workflow.__dict__)
    return new_workflow


async def get_workflow(workflow_id: UUID, is_template: bool = False) -> (Workflow | None):
    """Get workflow by id.

    Parameters
    ----------
    workflow_id
        Id of the requested workflow

    Returns
    -------
        Database orm model with data of requested workflow
    """
    async with async_session() as session:
        workflow = await session.get(WorkflowTemplates if is_template else WorkflowDefinitions, workflow_id)
    return workflow


async def get_all_workflows(exam_id: UUID, is_template: bool = False) -> list[Workflow]:
    """Get a list of all workflows assigned to a certain exam.

    Parameters
    ----------
    exam_id
        Id of the parent exam entry, workflows are assigned to

    Returns
    -------
        List of workflow data base orm models
    """
    async with async_session() as session:
        if is_template:
            result: Result = await session.execute(select(WorkflowTemplates).where(WorkflowTemplates.exam_id == exam_id))
        else:
            result: Result = await session.execute(select(WorkflowDefinitions).where(WorkflowDefinitions.exam_id == exam_id))
        workflows = list(result.scalars().all())
    return workflows


async def delete_workflow(workflow_id: UUID, is_template: bool = False) -> bool:
    """Delete a workflow by ID.

    Parameters
    ----------
    workflow_id
        ID of workflow to be deleted

    Returns
    -------
        Success of delete event
    """
    async with async_session() as session:
        if workflow := await session.get(WorkflowTemplates if is_template else WorkflowDefinitions, workflow_id):
            await session.delete(workflow)
            await session.commit()
            return True
        return False


async def update_workflow(workflow_id: UUID, payload: BaseWorkflow, is_template: bool = False) -> (Workflow | None):
    """Update existing workflow in database.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be updateed
    payload
        Workflow pydantic base model with data to be updated

    Returns
    -------
        Workflow database orm model of updated workflow
    """
    async with async_session() as session:
        if workflow := await session.get(WorkflowTemplates if is_template else WorkflowDefinitions, workflow_id):
            workflow.update(payload)
            await session.commit()
            await session.refresh(workflow)
            return workflow
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


async def get_all_tasks(workflow_id: UUID, is_template: bool = False) -> list[Task]:
    """Get a list of all tasks assigned to a certain workflow.

    Parameters
    ----------
    workflow_id
        Id of the parent workflow entry, tasks are assigned to

    Returns
    -------
        List of task data base orm models
    """
    async with async_session() as session:
        if is_template:
            result: Result = await session.execute(select(TaskTemplates).where(TaskTemplates.workflow_id == workflow_id))
        else:
            result: Result = await session.execute(select(TaskDefinitions).where(TaskDefinitions.workflow_id == workflow_id))
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
