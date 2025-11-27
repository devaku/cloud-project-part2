from azure.cosmos import CosmosClient

import azure.functions as func
import datetime
import json
import logging
import os

URL = os.environ['ACCOUNT_URI']
KEY = os.environ['ACCOUNT_KEY']
DATABASE_NAME = 'zdatabase'
CONTAINER_NAME = 'users'

client = CosmosClient(URL, credential=KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def findUserInDatabase(email, password):
    # Find if the user exists in the databse
    query = """
            SELECT * FROM c
            WHERE c.email = @email AND c.password = @password
            """

    result = container.query_items(
        query=query,
        parameters=[
            {"name": "@email", "value": email},
            {"name": "@password", "value": password}
        ],
        enable_cross_partition_query=True
    )
    
    # Returned value is an iterator that needs to be turned into a list
    result = list(result)
    return result    

def login(req: func.HttpRequest) -> func.HttpResponse:

    body = req.get_json()

    email = body.get('email') if body else ""
    password = body.get('password') if body else ""

    result = findUserInDatabase(email, password)
    
    if len(result) < 0:
        # Nothing found
        return func.HttpResponse(json.dumps({
            "status": "success",
            "message": "Given user was not found."
        }), mimetype="application/json")
    else:
        # Update entry to be logged in
        for item in result:
            item["isLoggedIn"] = 1

            # Replace the item back in Cosmos DB
            container.replace_item(item=item["id"], body=item)


    return func.HttpResponse(json.dumps({
        "status": "success",
        "isLoggedIn": 1
    }), mimetype="application/json")
        
def logout(req: func.HttpRequest) -> func.HttpResponse:

    body = req.get_json()

    email = body.get('email') if body else ""
    password = body.get('password') if body else ""
    
    result = findUserInDatabase(email, password)
    
    if len(result) < 0:
        # Nothing found
        return func.HttpResponse(json.dumps({
            "status": "success",
            "message": "Given user was not found."
        }), mimetype="application/json")
    else:
        # Update entry to be logged in
        for item in result:
            item["isLoggedIn"] = 0

            # Replace the item back in Cosmos DB
            container.replace_item(item=item["id"], body=item)


    return func.HttpResponse(json.dumps({
        "status": "success",
        "isLoggedIn": 0
    }), mimetype="application/json")

