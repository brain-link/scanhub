import os
import pytest
import requests
import numpy as np

# The base URL of the FastAPI server
BASE_URL = "http://localhost:8000"

# The endpoint path. Note that we'll format this string with the record_id
ENDPOINT_PATH = "/upload/{record_id}/"

# The test record_id to use
record_id = 1

# The path to the temporary file
file_path = 'test_upload.npy'

# Test fixture to create and remove a file
@pytest.fixture
def create_numpy_file():
    # Create a numpy array and save it to a file
    array_to_upload = np.array([1, 2, 3, 4, 5])
    np.save(file_path, array_to_upload)
    yield file_path
    os.remove(file_path)

# The actual test function
def test_upload_result(create_numpy_file):
    # Format the endpoint URL with the record_id
    endpoint = BASE_URL + ENDPOINT_PATH.format(record_id=record_id)

    # Define the files payload for the POST request
    with open(create_numpy_file, 'rb') as file:
        files = {'file': (os.path.basename(create_numpy_file), file.read())}

        # Send the POST request to the endpoint
        response = requests.post(endpoint, files=files)

    # Assertions to check if the upload was successful
    assert response.status_code == 200
    assert "Successfully uploaded" in response.json()['message']

# If you want to run the test with different record IDs
@pytest.mark.parametrize("record_id", [1, 2, 3])
def test_upload_multiple_records(create_numpy_file, record_id):
    endpoint = BASE_URL + ENDPOINT_PATH.format(record_id=record_id)
    with open(create_numpy_file, 'rb') as file:
        files = {'file': (os.path.basename(create_numpy_file), file.read())}
        response = requests.post(endpoint, files=files)

    assert response.status_code == 200
    assert "Successfully uploaded" in response.json()['message']
