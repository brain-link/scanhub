from api import app
# from database.models import Patient

@app.get("/")
async def root() -> dict:
    return dict(
        msg="Hello World!"
    )


# @api_router.get("/patients", status_code=200)
# async def get_patients() -> dict:
#     patients = Patient.all()
#     return dict(
#         data=[
#             dict(
#                 id=id,
#                 sex=patient.sex,
#                 birthday=patient.birthday,
#                 concern=patient.concern,
#                 admission_date=patient.admission_date,
#                 status=patient.status
#             ) for patient in patients
#         ]
#     )