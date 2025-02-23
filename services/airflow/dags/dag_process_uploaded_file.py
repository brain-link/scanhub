import os
from datetime import datetime, timedelta
import json
import numpy as np
from numpy.fft import fftshift, ifft2
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
        
        print(f"Verified file: {full_file_path}")
        return full_file_path

    @task()
    def reconstruct_image(file_path: str):
        """
        Task to reconstruct the image from k-space data using FFT.
        """
        print(f"Reading file: {file_path}")
        # Read the numpy array file
        kspace_data = np.load(file_path)
        print(f"K-space data shape: {kspace_data.shape}")

        # Perform FFT reconstruction
        image = np.abs(fftshift(ifft2(kspace_data)))
        print(f"Reconstructed image shape: {image.shape}")

        # Save the reconstructed image to a file
        image_file = file_path.replace(".npy", "_reconstructed.npy")
        np.save(image_file, image)
        return image_file

    @task()
    def save_results(image_file: str, output_path: str):
        """
        Task to save the reconstructed image.
        """
        if not os.path.exists(image_file):
            raise FileNotFoundError(f"File not found: {image_file}")

        # Load the reconstructed image from the file
        image = np.load(image_file)
        np.save(output_path, image)
        print(f"Reconstructed image saved to {output_path}")

    # Define the file paths
    data_lake_directory = '/opt/airflow/data_lake/'
    directory = '{{ dag_run.conf["directory"] }}'
    file_name = '{{ dag_run.conf["file_name"] }}'
    output_path = f"{data_lake_directory}/results/dag_process_uploaded_file/reconstructed_image.npy"

    # Define the task dependencies
    files = list_directory(f"{data_lake_directory}{directory}")
    kspace_data_file = read_file(f"{data_lake_directory}{directory}", file_name)
    image = reconstruct_image(kspace_data_file)
    save_results(image, output_path)