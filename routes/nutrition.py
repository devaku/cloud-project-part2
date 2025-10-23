from azure.storage.blob import BlobServiceClient
import azure.functions as func
import pandas as pd
import io
import json
import os



def processNutrition(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_name = 'datasets'
    blob_name = 'All_Diets.csv'
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    # Download blob content to bytes
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))
    
    # Calculate averages
    avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
    
    # Save results locally as JSON (simulate NoSQL storage)
    os.makedirs('simulated_nosql', exist_ok=True)
    result = avg_macros.reset_index().to_dict(orient='records')
    with open('simulated_nosql/results.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    return func.HttpResponse(f"{"Data processed and stored successfully."}")

def getAllData(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_name = 'datasets'
    blob_name = 'All_Diets.csv'
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    # Download blob content to bytes
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))
    result = df.reset_index().to_dict(orient='records')

    return func.HttpResponse(json.dumps(result), mimetype="application/json")