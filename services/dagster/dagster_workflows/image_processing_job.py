from dagster import job, op

@op
def load_data():
    return "raw k-space"

@op
def process(data):
    return f"Reconstructed image from {data}"

@job
def processing_job():
    process(load_data())
