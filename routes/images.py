import azure.functions as func
import logging
import os
from azure.storage.blob import BlobServiceClient

def fetch_image_from_blob(filename):
    """Download an image file from Azure Blob Storage."""
    conn_str = os.getenv("AzureWebJobsStorage")
    container_name = "images"  # Change if your container name is different

    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_data = blob_client.download_blob().readall()
    return blob_data

def getHeatmap(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fetching heatmap.png from Azure Blob Storage')
    try:
        data = fetch_image_from_blob("heatmap.png")
        return func.HttpResponse(data, mimetype="image/png")
    except Exception as e:
        logging.error(f"Error fetching heatmap.png: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)

def getBarchart(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fetching barchart.png from Azure Blob Storage')
    try:
        data = fetch_image_from_blob("barchart.png")
        return func.HttpResponse(data, mimetype="image/png")
    except Exception as e:
        logging.error(f"Error fetching barchart.png: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)

def getScatterplot(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fetching scatterplot.png from Azure Blob Storage')
    try:
        data = fetch_image_from_blob("scatterplot.png")
        return func.HttpResponse(data, mimetype="image/png")
    except Exception as e:
        logging.error(f"Error fetching scatterplot.png: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)
