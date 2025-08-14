"""Helper methods for workflows and exam, require recursive model translation."""

from fastapi import HTTPException
from scanhub_libraries.models import AcquisitionTaskOut, DAGTaskOut, ExamOut, ResultOut, WorkflowOut

from app.db.postgres import AcquisitionTask, DAGTask, Exam, Task, Workflow


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
    workflow["tasks"] = [await get_task_out(task) for task in data.tasks]
    return WorkflowOut(**workflow)


async def get_task_out(data: DAGTask | AcquisitionTask | Task) -> DAGTaskOut | AcquisitionTaskOut:
    """Transform db model to pydantic model.

    Parameters
    ----------
    data
        Task db model

    Returns
    -------
        Task pydantic model
    """
    task = data.__dict__
    task["results"] = [ResultOut(**result.__dict__) for result in data.results]

    if task["task_type"] == "ACQUISITION":
        return AcquisitionTaskOut(**task)
    elif task["task_type"] == "DAG":
        return DAGTaskOut(**task)
    else:
        raise HTTPException(status_code=400, detail="Invalid task type")
