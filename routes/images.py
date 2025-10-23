import azure.functions as func
import datetime
import json
import logging
import os

ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def getHeatmap(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file_path = ROOT_DIRECTORY + '/images/heatmap.png'
    print(file_path)

    with open(file_path, "rb") as f:
        data = f.read()
    return func.HttpResponse(data, mimetype="image/png")

def getBarchart(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file_path = ROOT_DIRECTORY + '/images/barchart.png'
    print(file_path)

    with open(file_path, "rb") as f:
        data = f.read()
    return func.HttpResponse(data, mimetype="image/png")

def getScatterplot(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file_path = ROOT_DIRECTORY + '/images/scatterplot.png'
    print(file_path)

    with open(file_path, "rb") as f:
        data = f.read()
    return func.HttpResponse(data, mimetype="image/png")