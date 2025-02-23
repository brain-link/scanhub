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
    def list_directory(directory: str):
        """
        Task to list files in a directory.
        """
        files = os.listdir(directory)
        print(f"Files in {directory}: {files}")
        return files

    @task()
    def read_file(directory: str, file_name: str):
        """
        Task to read the uploaded file.
        """
        full_file_path = f"{directory}/{file_name}"
        if not os.path.exists(full_file_path):
            raise FileNotFoundError(f"File not found: {full_file_path}")

        # Read the file (assuming it's a CSV for this example)
        df = pd.read_csv(full_file_path)
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
    data_lake_directory = '/opt/airflow/data_lake/'
    directory = '{{ dag_run.conf["directory"] }}'
    file_name = '{{ dag_run.conf["file_name"] }}'
    output_path = f"{data_lake_directory}/results/dag_process_uploaded_file/processing_results.json"

    # Define the task dependencies
    root_files = list_directory('/')
    data_lake_files = list_directory(data_lake_directory)
    files = list_directory(f"{data_lake_directory}{directory}")
    data = read_file(f"{data_lake_directory}{directory}", file_name)
    results = process_data(data)
    save_results(results, output_path)