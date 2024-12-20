# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of exam API endpoints accessible through swagger UI."""

from typing import Annotated
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import BaseExam, BaseTask, BaseWorkflow, ExamOut, ItemStatus, TaskOut, User, WorkflowOut
from scanhub_libraries.security import get_current_user

from app import dal
from app.db import Exam, Workflow

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

PREFIX_PATIENT_MANAGER = "http://patient-manager:8100/api/v1/patient"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
LOG_CALL_DELIMITER = "-------------------------------------------------------------------------------"


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


# Helper methods for workflows and exam, require recursive model translation
async def get_workflow_out_model(data: Workflow) -> WorkflowOut:
    """Transform db model to pydantic model.

    Parameters
    ----------
    data
        Workflow db model

    Returns
    -------
        Workflow pydantic model
    """
    workflow = data.__dict__
    workflow["tasks"] = [TaskOut(**task.__dict__) for task in data.tasks]
    return WorkflowOut(**workflow)


async def get_exam_out_model(data: Exam) -> ExamOut:
    """Transform db model to pydantic model.

    Parameters
    ----------
    data
        Exam db model

    Returns
    -------
        Exam pydantic model
    """
    exam = data.__dict__
    exam["workflows"] = [await get_workflow_out_model(workflow) for workflow in data.workflows]
    return ExamOut(**exam)


# ----- Exam API endpoints

@router.post("/new", response_model=ExamOut, status_code=201, tags=["exams"])
async def create_exam(payload: BaseExam,
                      user: Annotated[User, Depends(get_current_user)],
                      access_token: Annotated[str, Depends(oauth2_scheme)]) -> ExamOut:
    """Create a new exam.

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
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Payload:", payload)
    if payload.status != "NEW":
        raise HTTPException(status_code=400, detail="New exam needs to have status NEW.")
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given to create exam.")
        getpatient_response = requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3)
        if getpatient_response.status_code != 200:
            raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Exam template must not have patient_id.")
    if not (exam := await dal.add_exam_data(payload=payload, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create exam")
    return await get_exam_out_model(data=exam)


@router.post("/", response_model=ExamOut, status_code=201, tags=["exams"])
async def create_exam_from_template(payload: BaseExam, template_id: UUID,
                                    user: Annotated[User, Depends(get_current_user)],
                                    access_token: Annotated[str, Depends(oauth2_scheme)]) -> ExamOut:
    """Create a new exam from template.

    Parameters
    ----------
    payload
        The potentially modified exam to create.
    template_id
        ID of the template, the exam is created from

    Returns
    -------
        Exam pydantic output model.

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Exam:", payload)
    print("template_id:", template_id)
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given to create exam instance.")
        getpatient_response = requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3)
        if getpatient_response.status_code != 200:
            raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Exam template must not have patient_id.")
    if not (template := await dal.get_exam_data(exam_id=template_id)):
        raise HTTPException(status_code=400, detail="Template not found.")
    if template.is_template is not True:
        raise HTTPException(
            status_code=400,
            detail="Request to create exam from exam instance instead of exam template."
        )
    new_exam = BaseExam(**payload.__dict__)
    new_exam.status = 'NEW'
    if not (exam := await dal.add_exam_data(payload=new_exam, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create exam.")

    exam_out = await get_exam_out_model(data=exam)

    # Create all the sub-items for the workflow templates in the exam template
    for workflow in template.workflows:
        exam_out.workflows.append(await create_workflow_from_template(
            exam_id=exam.id,
            template_id=workflow.id,
            new_workflow_is_template=exam.is_template,
            user=user
        ))
    return exam_out


@router.get("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
async def get_exam(exam_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> ExamOut:
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
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    try:
        _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Badly formed exam_id")
    if not (exam := await dal.get_exam_data(exam_id=_id)):
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out_model(data=exam)


@router.get("/all/{patient_id}", response_model=list[ExamOut], status_code=200, tags=["exams"])
async def get_all_patient_exams(patient_id: UUID, user: Annotated[User, Depends(get_current_user)]) -> list[ExamOut]:
    """Get all exams of a certain patient.

    Parameters
    ----------
    patient_id
        Id of parent

    Returns
    -------
        List of exam pydantic output models
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("patient_id:", patient_id)
    if not (exams := await dal.get_all_exam_data(patient_id=patient_id)):
        # Don't raise exception here, list might be empty
        return []
    result = [await get_exam_out_model(data=exam) for exam in exams]
    print(">> Exam list: ", result)
    return result


@router.get("/templates/all", response_model=list[ExamOut], status_code=200, tags=["exams"])
async def get_all_exam_templates(user: Annotated[User, Depends(get_current_user)]) -> list[ExamOut]:
    """Get all exam templates.

    Returns
    -------
        List of exam pydantic output models
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if not (exams := await dal.get_all_exam_template_data()):
        # Don't raise exception here, list might be empty
        return []
    result = [await get_exam_out_model(data=exam) for exam in exams]
    print("Number of exam templates: ", len(result))
    return result


@router.delete("/{exam_id}", response_model={}, status_code=204, tags=["exams"])
async def exam_delete(exam_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> None:
    """Delete an exam by id. Cascade deletes the associated workflow and tasks.

    Parameters
    ----------
    exam_id
        Id of the exam to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not await dal.delete_exam_data(exam_id=_id):
        message = "Could not delete exam, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)


@router.put("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
async def update_exam(exam_id: UUID | str, payload: BaseExam,
                      user: Annotated[User, Depends(get_current_user)],
                      access_token: Annotated[str, Depends(oauth2_scheme)]) -> ExamOut:
    """Update an existing exam.

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
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given for exam instance.")
        getpatient_response = requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3)
        if getpatient_response.status_code != 200:
            raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
        # for now, allow changing the patient_id, but could require administrator rights in the future
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Exam template must not have patient_id.")
    # for now allow changing is_template in principle, but that could be refused in the future
    if payload.status == "NEW":
        raise HTTPException(status_code=403, detail="Exam cannot be updated to status NEW.")
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not (exam_updated := await dal.update_exam_data(exam_id=_id, payload=payload)):
        message = "Could not update exam, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)
    return await get_exam_out_model(data=exam_updated)


# ----- Workflow API endpoints

@router.post("/workflow/new", response_model=WorkflowOut, status_code=201, tags=["workflows"])
async def create_workflow(payload: BaseWorkflow, user: Annotated[User, Depends(get_current_user)]) -> WorkflowOut:
    """Create new workflow.

    Parameters
    ----------
    payload
        Workflow pydantic input model

    Returns
    -------
        Workflow pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("payload:", payload)
    if payload.status != "NEW":
        raise HTTPException(status_code=400, detail="New workflow needs to have status NEW.")
    if payload.exam_id is not None:
        _id = UUID(payload.exam_id) if not isinstance(payload.exam_id, UUID) else payload.exam_id
        if not (exam := await dal.get_exam_data(exam_id=_id)):
            raise HTTPException(status_code=400, detail="exam_id must be an existing id.")
        if exam.is_template != payload.is_template:
            raise HTTPException(
                status_code=400,
                detail="Invalid link to exam. Instance needs to refer to instance, template to template."
            )
    if payload.is_template is False and payload.exam_id is None:
        raise HTTPException(status_code=400, detail="Workflow instance needs exam_id.")
    if not (workflow := await dal.add_workflow_data(payload=payload, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create workflow")
    print("New workflow: ", workflow)
    return await get_workflow_out_model(data=workflow)


@router.post("/workflow", response_model=WorkflowOut, status_code=201, tags=["workflows"])
async def create_workflow_from_template(exam_id: UUID,
                                        template_id: UUID,
                                        new_workflow_is_template: bool,
                                        user: Annotated[User, Depends(get_current_user)]) -> WorkflowOut:
    """Create new workflow from template.

    Parameters
    ----------
    exam_id
        Id of the exam, the workflow is related to
    template_id
        ID of the template, the workflow is created from
    new_workflow_is_template
        set the is_template property of the new workflow and its tasks

    Returns
    -------
        Workflow pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    print("template_id:", template_id)
    print("new_workflow_is_template:", new_workflow_is_template)
    if not (template := await dal.get_workflow_data(workflow_id=template_id)):
        raise HTTPException(status_code=404, detail="Workflow not found")
    if template.is_template is not True:
        raise HTTPException(
            status_code=400,
            detail="Request to create workflow from workflow instance instead of workflow template."
        )
    new_workflow = BaseWorkflow(**template.__dict__)
    new_workflow.status = "NEW"
    new_workflow.is_template = new_workflow_is_template
    new_workflow.exam_id = exam_id
    if not (exam := await dal.get_exam_data(exam_id=exam_id)):
        raise HTTPException(status_code=400, detail="exam_id must be an existing id.")
    if exam.is_template != new_workflow_is_template:
        raise HTTPException(
            status_code=400,
            detail="Invalid link to exam. Instance needs to refer to instance, template to template."
        )
    if not (workflow := await dal.add_workflow_data(payload=new_workflow, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create workflow.")

    workflow_out = await get_workflow_out_model(data=workflow)

    # Create all the sub-items for the task templates in a workflow template
    for task in template.tasks:
        workflow_out.tasks.append(await create_task_from_template(
            workflow_id=workflow.id,
            template_id=task.id,
            new_task_is_template=new_workflow_is_template,
            user=user
        ))

    return workflow_out


@router.get("/workflow/{workflow_id}", response_model=WorkflowOut, status_code=200, tags=["workflows"])
async def get_workflow(workflow_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> WorkflowOut:
    """Get a workflow.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be returned

    Returns
    -------
        Workflow pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("workflow_id:", workflow_id)
    try:
        _id = UUID(workflow_id) if not isinstance(workflow_id, UUID) else workflow_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Badly formed workflow_id.")
    if not (workflow := await dal.get_workflow_data(workflow_id=_id)):
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await get_workflow_out_model(data=workflow)


@router.get(
    "/workflow/all/{exam_id}",
    response_model=list[WorkflowOut],
    status_code=200,
    tags=["workflows"],
)
async def get_all_exam_workflows(
    exam_id: UUID | str,
    user: Annotated[User, Depends(get_current_user)]) -> list[WorkflowOut]:
    """Get all existing workflows of a certain exam.

    Parameters
    ----------
    exam_id
        Id of parent exam

    Returns
    -------
        List of workflow pydantic output model
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not (workflows := await dal.get_all_workflow_data(exam_id=_id)):
        # Don't raise exception, list might be empty
        return []
    return [await get_workflow_out_model(data=workflow) for workflow in workflows]


@router.get(
    "/workflow/templates/all",
    response_model=list[WorkflowOut],
    status_code=200,
    tags=["workflows"],
)
async def get_all_workflow_templates(user: Annotated[User, Depends(get_current_user)]) -> list[WorkflowOut]:
    """Get all workflow templates.

    Returns
    -------
        List of workflow pydantic output model
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if not (workflows := await dal.get_all_workflows_template_data()):
        # Don't raise exception, list might be empty
        return []
    return [await get_workflow_out_model(data=workflow) for workflow in workflows]


@router.delete("/workflow/{workflow_id}", response_model={}, status_code=204, tags=["workflows"])
async def delete_workflow(workflow_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> None:
    """Delete a workflow. Cascade delete the associated tasks.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("workflow_id:", workflow_id)
    _id = UUID(workflow_id) if not isinstance(workflow_id, UUID) else workflow_id
    if not await dal.delete_workflow_data(workflow_id=_id):
        message = "Could not delete workflow, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)


@router.put("/workflow/{workflow_id}", response_model=WorkflowOut, status_code=200, tags=["workflows"])
async def update_workflow(workflow_id: UUID | str, payload: BaseWorkflow,
                          user: Annotated[User, Depends(get_current_user)]) -> WorkflowOut:
    """Update an existing workflow.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be updated
    payload
        Workflow pydantic indput model

    Returns
    -------
        Workflow pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("workflow_id:", workflow_id)
    print("payload:", payload)
    if payload.status == "NEW":
        raise HTTPException(status_code=403, detail="Workflow cannot be updated to status NEW.")
    if payload.exam_id is not None:
        exam_id = UUID(payload.exam_id) if not isinstance(payload.exam_id, UUID) else payload.exam_id
        if not (exam := await dal.get_exam_data(exam_id=exam_id)):
            raise HTTPException(status_code=400, detail="exam_id must be an existing id.")
        if exam.is_template != payload.is_template:
            raise HTTPException(
                status_code=400,
                detail="Invalid link to exam. Instance needs to refer to instance, template to template."
            )
    if payload.is_template is False and payload.exam_id is None:
        raise HTTPException(status_code=400, detail="Workflow instance needs exam_id.")
    _id = UUID(workflow_id) if not isinstance(workflow_id, UUID) else workflow_id
    if not (workflow := await dal.get_workflow_data(workflow_id=_id)):
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not (workflow := await dal.update_workflow_data(workflow_id=_id, payload=payload)):
        raise HTTPException(status_code=404, detail="Workflow could not be updated.")
    return await get_workflow_out_model(data=workflow)


# ----- Task API endpoints

@router.post("/task/new", response_model=TaskOut, status_code=201, tags=["tasks"])
async def create_task(payload: BaseTask, user: Annotated[User, Depends(get_current_user)]) -> TaskOut:
    """Create a new task.

    Parameters
    ----------
    payload
        Task pydantic input model

    Returns
    -------
        Task pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("payload:", payload)
    if payload.status != ItemStatus.NEW:
        raise HTTPException(status_code=400, detail="New task needs to have status NEW")
    if payload.workflow_id is not None:
        workflow_id = UUID(payload.workflow_id) if not isinstance(payload.workflow_id, UUID) else payload.workflow_id
        if not (workflow := await dal.get_workflow_data(workflow_id=workflow_id)):
            raise HTTPException(status_code=400, detail="workflow_id must be an existing id.")
        if workflow.is_template != payload.is_template:
            raise HTTPException(
                status_code=400,
                detail="Invalid link to workflow. Instance needs to refer to instance, template to template."
            )
    if payload.is_template is False and payload.workflow_id is None:
        raise HTTPException(status_code=400, detail="Task instance needs workflow_id.")
    if not (task := await dal.add_task_data(payload=payload, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create task")
    result = TaskOut(**task.__dict__)
    print("Task created: ", result)
    return result


@router.post("/task", response_model=TaskOut, status_code=201, tags=["tasks"])
async def create_task_from_template(workflow_id: UUID, template_id: UUID, new_task_is_template: bool,
                                    user: Annotated[User, Depends(get_current_user)]) -> TaskOut:
    """Create a new task from template.

    Parameters
    ----------
    workflow_id
        ID of the workflow, the task is related to
    template_id
        ID of the template, the task is created from
    new_task_is_template
        set the is_template property on the new task

    Returns
    -------
        Task pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("workflow_id:", workflow_id)
    print("template_id:", template_id)
    print("new_task_is_template:", new_task_is_template)
    if not (template := await dal.get_task_data(task_id=template_id)):
        raise HTTPException(status_code=404, detail="Task template not found")
    if template.is_template is not True:
        raise HTTPException(
            status_code=400,
            detail="Request to create task from task instance instead of task template."
        )
    new_task = BaseTask(**template.__dict__)
    # if not TaskStatus.PENDING in new_task.status:
    #     new_task[TaskStatus.PENDING] = "New task instance."
    new_task.is_template = new_task_is_template
    new_task.workflow_id = workflow_id
    if not (workflow := await dal.get_workflow_data(workflow_id=workflow_id)):
        raise HTTPException(status_code=400, detail="workflow_id must be an existing id.")
    if workflow.is_template != new_task_is_template:
        raise HTTPException(
            status_code=400,
            detail="Invalid link to workflow. Instance needs to refer to instance, template to template."
        )
    if not (task := await dal.add_task_data(payload=new_task, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create task.")
    result = TaskOut(**task.__dict__)
    print("Task created: ", result)
    return result


@router.get("/task/{task_id}", response_model=TaskOut, status_code=200, tags=["tasks"])
async def get_task(task_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> TaskOut:
    """Get an existing task.

    Parameters
    ----------
    task_id
        Id of the task to be returned

    Returns
    -------
        Task pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("task_id:", task_id)
    try:
        _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Badly formed task_id.")
    if not (task := await dal.get_task_data(task_id=_id)):
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut(**task.__dict__)


@router.get(
    "/task/all/{workflow_id}",
    response_model=list[TaskOut],
    status_code=200,
    tags=["tasks"],
)
async def get_all_workflow_tasks(
    workflow_id: UUID | str,
    user: Annotated[User, Depends(get_current_user)]) -> list[TaskOut]:
    """Get all existing tasks of a certain workflow.

    Parameters
    ----------
    workflow_id
        Id of parental workflow

    Returns
    -------
        List of task pydantic output model
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("workflow_id:", workflow_id)
    _id = UUID(workflow_id) if not isinstance(workflow_id, UUID) else workflow_id
    if not (tasks := await dal.get_all_task_data(workflow_id=_id)):
        # Don't raise exception here, list might be empty.
        return []
    result = [TaskOut(**task.__dict__) for task in tasks]
    print("List of tasks: ", result)
    return result

@router.get(
    "/task/templates/all",
    response_model=list[TaskOut],
    status_code=200,
    tags=["tasks"],
)
async def get_all_task_templates(user: Annotated[User, Depends(get_current_user)]) -> list[TaskOut]:
    """Get all existing task templates.

    Returns
    -------
        List of task pydantic output model
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if not (tasks := await dal.get_all_task_template_data()):
        # Don't raise exception here, list might be empty.
        return []
    result = [TaskOut(**task.__dict__) for task in tasks]
    print("List of tasks: ", result)
    return result


@router.delete("/task/{task_id}", response_model={}, status_code=204, tags=["tasks"])
async def delete_task(task_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> None:
    """Delete a task.

    Parameters
    ----------
    task_id
        Id of the task to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("task_id:", task_id)
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not await dal.delete_task_data(task_id=_id):
        message = "Could not delete task, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)


@router.put("/task/{task_id}", response_model=TaskOut, status_code=200, tags=["tasks"])
async def update_task(task_id: UUID | str, payload: BaseTask,
                      user: Annotated[User, Depends(get_current_user)]) -> TaskOut:
    """Update an existing task.

    Parameters
    ----------
    task_id
        Id of the workflow to be updated
    payload
        Task pydantic base model

    Returns
    -------
        Task pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("task_id:", task_id)
    # if TaskStatus.PENDING in payload.status:
    #     raise HTTPException(status_code=400, detail="Task must not update to status PENDING "
    if payload.workflow_id is not None:
        workflow_id = UUID(payload.workflow_id) if not isinstance(payload.workflow_id, UUID) else payload.workflow_id
        if not (workflow := await dal.get_workflow_data(workflow_id=workflow_id)):
            raise HTTPException(status_code=400, detail="workflow_id must be an existing id.")
        if workflow.is_template != payload.is_template:
            raise HTTPException(
                status_code=400,
                detail="Invalid link to workflow. Instance needs to refer to instance, template to template."
            )
    if payload.is_template is False and payload.workflow_id is None:
        raise HTTPException(status_code=400, detail="Task instance needs workflow_id.")
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not (task_updated := await dal.update_task_data(task_id=_id, payload=payload)):
        message = "Could not update workflow, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)
    return TaskOut(**task_updated.__dict__)
