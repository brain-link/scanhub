import logging
import os
from azure.storage.blob import BlobServiceClient
from azure.cosmosdb.table.tableservice import TableService

##############
# BLOB STORAGE
##############


# Creates a blob service client
def create_blob_service_client(connection_string):
    blob_service_client = None
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        logging.info("Created blob service client.")
    except Exception as e:
        logging.error(f"Could not create blob service client: {e}")
    return blob_service_client

# Downloads the specified blob
def download_blob(container_name, blob_name, connection_string):
    blob_service_client = create_blob_service_client(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    try:
        if blob_client.exists():
            downloads_folder = "downloads"
            local_path = downloads_folder + '/' + blob_name
            if not os.path.exists(downloads_folder):
                os.makedirs(downloads_folder)
            with open(local_path, "wb") as f:
                stream = blob_client.download_blob()
                f.write(stream.readall())
            return local_path
        else:
            logging.error(f"Blob {blob_name} doesn't exist.")
    except ResourceNotFoundError:
        logging.error(f"The blob {blob_name} was not found.")
    return None


# Creates a blob in blob storage from bytes
def upload_blob(container_name, blob_name, data, connection_string):
    blob_service_client = create_blob_service_client(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    try:
        blob_client.upload_blob(data=data)
        logging.info(f"Created blob {blob_name} successfully.")
        return True
    except Exception:
        try:
            blob_client.delete_blob()
            blob_client.upload_blob(data=data)
            logging.warning(f"Blob {blob_name} already exists, deleted it.")
            logging.info(f"Created blob {blob_name} successfully.")
            return True
        except Exception as e:
            logging.error(f"Error creating blob {blob_name}: {e}")
    return False


###############
# TABLE STORAGE
###############


# Creates an Azure Table Storage service
def create_table_service(connection_string):
    table_service = None
    try:
        table_service = TableService(connection_string=connection_string)
    except Exception as e:
        logging.error(f"Could not instantiate table service: {e}")
    return table_service


# Creates an entity if it doesn't exist, updates its status if it does
def update_status(table_name, item_name, status, connection_string):
    table_service = create_table_service(connection_string)
    try:
        entity = {
            "PartitionKey": item_name[0], 
            "RowKey": item_name,
            "status": status 
        }
        table_service.insert_or_replace_entity(table_name, entity)
        logging.info(f"Set status for item {item_name} to {status}.")
        return True
    except Exception as e:
        logging.error(f"Could not insert or update entity in table {table_name}:{e}")
        return False
