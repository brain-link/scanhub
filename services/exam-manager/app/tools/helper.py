"""Helper methods for workflows and exam, require recursive model translation."""

from scanhub_libraries.models import AcquisitionTaskOut, ExamOut, ResultOut, WorkflowOut

from app.db.postgres import AcquisitionTask, Exam, Workflow


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


async def get_task_out(data: AcquisitionTask) -> AcquisitionTaskOut:
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
    return AcquisitionTaskOut(**task)
