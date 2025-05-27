# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data acess layer (DAL) between fastapi endpoint and sql database."""

from pprint import pprint
from uuid import UUID

from scanhub_libraries.models import BaseExam
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from app.db import (
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
    new_exam = Exam(**payload.dict(), creator=creator)
    async with async_session() as session:
        session.add(new_exam)
        await session.commit()
        await session.refresh(new_exam)
    # debug
    print("***** NEW EXAM *****")
    pprint(new_exam.__dict__)
    return new_exam


async def get_exam_data(exam_id: UUID) -> (Exam | None):
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


async def update_exam_data(exam_id: UUID, payload: BaseExam) -> (Exam | None):
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


# # ----- Workflow data access layer

# async def add_workflow_data(payload: BaseWorkflow, creator: str) -> Workflow:
#     """Add new workflow.

#     Parameters
#     ----------
#     payload
#         Workflow pydantic base model with data for workflow creation
#     creator
#         The username/id of the user who creats this exam

#     Returns
#     -------
#         Database orm model of created workflow
#     """
#     new_workflow = Workflow(**payload.dict(), creator=creator)
#     async with async_session() as session:
#         session.add(new_workflow)
#         await session.commit()
#         await session.refresh(new_workflow)
#     # Debugging
#     print("***** NEW WORKFLOW *****")
#     pprint(new_workflow.__dict__)
#     return new_workflow


# async def get_workflow_data(workflow_id: UUID) -> (Workflow | None):
#     """Get workflow by id.

#     Parameters
#     ----------
#     workflow_id
#         Id of the requested workflow

#     Returns
#     -------
#         Database orm model with data of requested workflow
#     """
#     async with async_session() as session:
#         workflow = await session.get(Workflow, workflow_id)
#     return workflow


# async def get_all_workflow_data(exam_id: UUID) -> list[Workflow]:
#     """Get a list of all workflows assigned to a certain exam.

#     Parameters
#     ----------
#     exam_id
#         Id of the parent exam entry, workflows are assigned to

#     Returns
#     -------
#         List of workflow data base orm models
#     """
#     async with async_session() as session:
#         result: Result = await session.execute(select(Workflow).where(Workflow.exam_id == exam_id))
#         workflows = list(result.scalars().all())
#     return workflows


# async def get_all_workflows_template_data() -> list[Workflow]:
#     """Get a list of all workflows assigned to a certain exam.

#     Parameters
#     ----------
#     exam_id
#         Id of the parent exam entry, workflows are assigned to

#     Returns
#     -------
#         List of workflow data base orm models
#     """
#     async with async_session() as session:
#         result: Result = await session.execute(select(Workflow).where(Workflow.is_template))
#         workflows = list(result.scalars().all())
#     return workflows


# async def delete_workflow_data(workflow_id: UUID) -> bool:
#     """Delete a workflow by ID. Cascade delete the associated tasks.

#     Parameters
#     ----------
#     workflow_id
#         ID of workflow to be deleted

#     Returns
#     -------
#         Success of delete event
#     """
#     async with async_session() as session:
#         if workflow := await session.get(Workflow, workflow_id):
#             for task in workflow.tasks:
#                 await session.delete(task)
#             await session.delete(workflow)
#             await session.commit()
#             return True
#         return False


# async def update_workflow_data(workflow_id: UUID, payload: BaseWorkflow) -> (Workflow | None):
#     """Update existing workflow in database.

#     Parameters
#     ----------
#     workflow_id
#         Id of the workflow to be updateed
#     payload
#         Workflow pydantic base model with data to be updated

#     Returns
#     -------
#         Workflow database orm model of updated workflow
#     """
#     async with async_session() as session:
#         if workflow := await session.get(Workflow, workflow_id):
#             workflow.update(payload)
#             await session.commit()
#             await session.refresh(workflow)
#             return workflow
#         return None


# # ----- Task data access layer

# async def add_task_data(payload: BaseTask, creator) -> Task:
#     """Add new task to database.

#     Parameters
#     ----------
#     payload
#         Task pydantic base model
#     creator
#         The username/id of the user who creats this task

#     Returns
#     -------
#         Database orm model of created task
#     """
#     new_task = Task(**payload.dict(), creator=creator)
#     async with async_session() as session:
#         session.add(new_task)
#         await session.commit()
#         await session.refresh(new_task)
#     return new_task


# async def get_task_data(task_id: UUID) -> (Task | None):
#     """Get task by id.

#     Parameters
#     ----------
#     task_id
#         Id of the requested task

#     Returns
#     -------
#         Database orm model with data of requested task
#     """
#     async with async_session() as session:
#         task = await session.get(Task, task_id)
#     return task


# async def get_all_task_data(workflow_id: UUID) -> list[Task]:
#     """Get a list of all tasks assigned to a certain workflow.

#     Parameters
#     ----------
#     workflow_id
#         Id of the parent workflow entry, tasks are assigned to

#     Returns
#     -------
#         List of task data base orm models
#     """
#     async with async_session() as session:
#         result: Result = await session.execute(select(Task).where(Task.workflow_id == workflow_id))
#         tasks = list(result.scalars().all())
#     return tasks


# async def get_all_task_template_data() -> list[Task]:
#     """Get a list of all tasks assigned to a certain workflow.

#     Parameters
#     ----------
#     workflow_id
#         Id of the parent workflow entry, tasks are assigned to

#     Returns
#     -------
#         List of task data base orm models
#     """
#     async with async_session() as session:
#         result: Result = await session.execute(select(Task).where(Task.is_template))
#         tasks = list(result.scalars().all())
#     return tasks


# async def delete_task_data(task_id: UUID) -> bool:
#     """Delete task by id.

#     Parameters
#     ----------
#     task_id
#         Id of the task to be deleted

#     Returns
#     -------
#         Success of deletion
#     """
#     async with async_session() as session:
#         if task := await session.get(Task, task_id):
#             await session.delete(task)
#             await session.commit()
#             return True
#         return False


# async def update_task_data(task_id: UUID, payload: BaseTask) -> (Task | None):
#     """Update existing task in database.

#     Parameters
#     ----------
#     task_id
#         Id of the task to be updateed
#     payload
#         Task pydantic base model with data to be updated

#     Returns
#     -------
#         Database orm model of updated task
#     """
#     async with async_session() as session:
#         if task := await session.get(Task, task_id):
#             task.update(payload)
#             await session.commit()
#             await session.refresh(task)
#             return task
#         return None
