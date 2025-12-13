import os
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient

def read_csv_from_blob():
    conn_str = os.getenv("AzureWebJobsStorage")
    container_name = "datasets"   # adjust if different
    blob_name = "All_Diets.csv"

    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    csv_bytes = blob_client.download_blob().readall()
    df = pd.read_csv(StringIO(csv_bytes.decode('utf-8')))
    return df
