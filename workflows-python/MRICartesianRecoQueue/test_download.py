import logging
import storage_helpers

file_name = "sample_file1.txt"
logging.info(f"### Processing queue item: {file_name}...")

# Getting settings
STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;" #os.getenv("STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "testdocs" #os.getenv("STORAGE_CONTAINER_NAME")
TABLE_NAME = "status" #os.getenv("STORAGE_TABLE_NAME")

print(f"### STORAGE_CONNECTION_STRING: {STORAGE_CONNECTION_STRING}")
print(f"### CONTAINER_NAME: {CONTAINER_NAME}")
print(f"### TABLE_NAME: {TABLE_NAME}")

# # Updating status to new
# storage_helpers.update_status(TABLE_NAME, file_name, 'new', STORAGE_CONNECTION_STRING)

# Getting file from storage
file_path = storage_helpers.download_blob(CONTAINER_NAME, file_name, STORAGE_CONNECTION_STRING)

print(file_path)
