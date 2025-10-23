import azure.functions as func
import datetime
import json
import logging
import os

def debug(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return func.HttpResponse(f"{file_path}")
        
