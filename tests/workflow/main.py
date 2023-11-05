import os
import requests
import numpy as np

# Define the URL of the endpoint
URL = "http://localhost:8080//api/v1/workflow/upload/{record_id}/"

# The ID of the record being processed
record_id = 1

# Create a numpy array and save it to a file
array_to_upload = np.array([1, 2, 3, 4, 5])
file_path = 'test_upload.npy'
np.save(file_path, array_to_upload)

# Define the test function
def test_upload_result():
    # Replace `{record_id}` in the URL with the actual `record_id`
    endpoint = URL.format(record_id=record_id)

    # Read the binary content of the file
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Define the files payload for the POST request
    files = {'file': (os.path.basename(file_path), file_data)}

    # Send the POST request to the endpoint
    response = requests.post(endpoint, files=files)

    # Clean up the file now that we're done with it
    os.remove(file_path)

    # Check if the request was successful
    assert response.status_code == 200
    assert "Successfully uploaded" in response.json()['message']

# Call the test function
test_upload_result()
