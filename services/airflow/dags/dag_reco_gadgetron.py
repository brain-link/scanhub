import os
from datetime import datetime, timedelta
import numpy as np
from numpy.fft import fftshift, ifft2
from airflow import DAG
from airflow.decorators import task
import requests
from zipfile import ZipFile, is_zipfile

# [END import_module]

default_args = {
    'owner': 'Patrick Hucker',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
with DAG(
    dag_id='dag_reco_gadgetron',
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
    def create_directories(*directories: str):
        """
        Task to create necessary directories.
        """
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            else:
                print(f"Directory already exists: {directory}")

    @task()
    def read_file(file_path: str, file_name: str):
        """
        Task to read the uploaded file.
        """
        input_file_path = f"{file_path}/{file_name}"
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"File not found: {input_file_path}")
        
        print(f"Verified file: {input_file_path}")
        return input_file_path

    @task()
    def extract_zip_file(input_file_path: str, temporary_path: str):
        """
        Task to extract the zip file.
        """
        if is_zipfile(input_file_path):
            with ZipFile(input_file_path, 'r') as zip_ref:
                zip_ref.extractall(temporary_path)
                print(f"Extracted file: {input_file_path}")
            return temporary_path
        else:
            print(f"File is not a zip file: {input_file_path}")
            return input_file_path

    @task()
    def reco_via_gadgetron(raw_ismrmrd_file: str, reco_config_file: str):
        """
        Task to reconstruct the image from a raw ismrmrd file using Gadgetron.
        """
        
        print(f"Reconstructing image from {raw_ismrmrd_file} using {reco_config_file}")

        # Call Gadgetron to reconstruct the image
        # This is a placeholder for the actual reconstruction code
        # The reconstructed image is saved to a file

        return image_file

    @task()
    def save_results(output_path: str, image_file: str):
        """
        Task to save the reconstructed image.
        """
        if not os.path.exists(image_file):
            raise FileNotFoundError(f"File not found: {image_file}")

        # Load the reconstructed image from the file
        image = np.load(image_file)

        # Save the reconstructed image to a file
        result_file = f"{output_path}/reconstructed_image.npy"
        np.save(result_file, image)
        print(f"Reconstructed image saved to {output_path}")
        return result_file

    @task()
    def notify_workflow_manager(endpoint: str, result_file: str, user_token: str, **context):
        """
        Task to notify the workflow manager that the results are ready.
        """
        print(f"Notifying workflow manager: {endpoint}")
        payload = {
            "dag_id": context['dag'].dag_id,
            "result_file": result_file
        }
        response = requests.post(endpoint, json=payload, headers={'Authorization': 'Bearer ' + user_token})
        if response.status_code != 200:
            raise Exception(f"Failed to notify workflow manager: {response.status_code}")
        print(f"Notified workflow manager: {response.text}")

    # Define the file paths
    data_lake_path = os.getenv('DATA_LAKE_DIRECTORY', '/opt/airflow/data_lake')
    INPUT_DIR = '{{ dag_run.conf["directory"] }}'
    INPUT_FILE = '{{ dag_run.conf["file_name"] }}'
    WORKFLOW_MANAGER_ENDPOINT = '{{ dag_run.conf["workflow_manager_endpoint"] }}'
    USER_TOKEN = '{{ dag_run.conf["user_token"] }}'

    input_path = f"{data_lake_path}{INPUT_DIR}"
    temporary_path = f"{data_lake_path}/temp/dag_process_uploaded_file"
    output_path = f"{data_lake_path}/results/dag_process_uploaded_file"

    # Define the task dependencies
    files = list_directory(input_path)
    create_dirs = create_directories(temporary_path, output_path)
    input_file_path = read_file(input_path, INPUT_FILE)
    extracted_path = extract_zip_file(input_file_path, temporary_path)
    image_file = reco_via_gadgetron(temporary_path, extracted_path)
    result_file = save_results(output_path, image_file)
    notify_workflow_manager_task = notify_workflow_manager(WORKFLOW_MANAGER_ENDPOINT, result_file, USER_TOKEN)
