import os
from datetime import datetime, timedelta
import json
import pandas as pd

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'BRAIN-LINK',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
with DAG(
    dag_id='dag_process_uploaded_file',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['scanhub', 'processing']
) as dag:

    @task()
    def read_file(file_path: str):
        """
        Task to read the uploaded file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read the file (assuming it's a CSV for this example)
        df = pd.read_csv(file_path)
        print(f"File content:\n{df.head()}")
        return df.to_json()

    @task()
    def process_data(data: str):
        """
        Task to process the data.
        """
        df = pd.read_json(data)
        # Perform some processing (example: calculate the mean of a column)
        result = df.mean().to_dict()
        print(f"Processing result: {result}")
        return result

    @task()
    def save_results(results: dict, output_path: str):
        """
        Task to save the processing results.
        """
        with open(output_path, 'w') as f:
            json.dump(results, f)
        print(f"Results saved to {output_path}")

    # Define the file paths
    file_path = '{{ dag_run.conf["file_path"] }}'
    output_path = '/opt/airflow/data_lake/results/dag_process_uploaded_file/processing_results.json'

    # Define the task dependencies
    data = read_file(file_path)
    results = process_data(data)
    save_results(results, output_path)