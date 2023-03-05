from api.models import ExamIn, ExamOut, ExamUpdate
from api.db import exam, database


async def add_exam(payload: ExamIn):
    pass
    query = exam.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_exam(id):
    pass
    query = exam.select(exam.c.id==id)
    return await database.fetch_one(query=query)
