from azure.cosmos import CosmosClient

import azure.functions as func
import datetime
import json
import logging
import bcrypt
import os

URL = os.environ['ACCOUNT_URI']
KEY = os.environ['ACCOUNT_KEY']
DATABASE_NAME = 'zdatabase'
CONTAINER_NAME = 'users'
SALT = b'$2b$12$dwPD515/oDfrW0GPTxTXvO'

client = CosmosClient(URL, credential=KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def findUserInDatabase(email):
    # Find if the user exists in the databse
    query = """
            SELECT * FROM c
            WHERE c.email = @email
            """

    result = container.query_items(
        query=query,
        parameters=[
            {"name": "@email", "value": email},
        ],
        enable_cross_partition_query=True
    )
    
    # Returned value is an iterator that needs to be turned into a list
    result = list(result)

    return result    

def getAllUsers():
    query = """
            SELECT * FROM users
            """

    result = container.query_items(
        query=query,
        enable_cross_partition_query=True
    )
    
    # Returned value is an iterator that needs to be turned into a list
    result = list(result)
    return result    

def hashPassword(password):
    encoded_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, SALT)
    return hashed_password.decode('utf-8')


def verifyPassword(password, hashedValue):
    if bcrypt.checkpw(password.encode('utf-8'), hashedValue.encode('utf-8')):
        return True
    else:
        return False

def register(req: func.HttpRequest) -> func.HttpResponse:

    body = req.get_json()

    email = body.get('email') if body else ""
    password = body.get('password') if body else ""
    password = hashPassword(password)

    result = findUserInDatabase(email)
    
    if len(result) < 0:
        # Nothing found
        return func.HttpResponse(json.dumps({
            "status": "fail",
            "message": "User already exist."
        }), mimetype="application/json")
    else:
        # Get the latest ID from the database
        usersRows = getAllUsers()
        listOfIds = [x['id'] for x in usersRows]
        latestId = 0
        if (len(listOfIds) == 0):
            latestId = 1
        else:
            latestId = int(listOfIds[-1]) + 1

        # Insert item
        container.upsert_item({
            'id': str(latestId),
            'email': email,
            'password': password,
            'isLoggedIn': 0
        })

    return func.HttpResponse(json.dumps({
        "status": "success",
        "message": "User successfully registered."
    }), mimetype="application/json")

def login(req: func.HttpRequest) -> func.HttpResponse:

    body = req.get_json()

    email = body.get('email') if body else ""
    password = body.get('password') if body else ""

    result = findUserInDatabase(email)
    
    if len(result) < 0:
        # Nothing found
        return func.HttpResponse(json.dumps({
            "status": "fail",
            "message": "Given user was not found."
        }), mimetype="application/json")
    else:
        # Update entry to be logged in
        item = result[0]
        dbPassword = item["password"]

        if verifyPassword(password, dbPassword):    
            item["isLoggedIn"] = 1

            # Replace the item back in Cosmos DB
            container.replace_item(item=item["id"], body=item)
        else:
            return func.HttpResponse(json.dumps({
                "status": "fail",
                "message": "Invalid user credentials."
                }), mimetype="application/json")

    return func.HttpResponse(json.dumps({
        "status": "success",
        "isLoggedIn": 1
    }), mimetype="application/json")
        
def logout(req: func.HttpRequest) -> func.HttpResponse:

    body = req.get_json()

    email = body.get('email') if body else ""
    password = body.get('password') if body else ""
    password = hashPassword(password)

    result = findUserInDatabase(email)
    
    if len(result) < 0:
        # Nothing found
        return func.HttpResponse(json.dumps({
            "status": "fail",
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

def verifyLogin(req: func.HttpRequest) -> func.HttpResponse:

    body = req.get_json()
    email = body.get('email') if body else ""
    result = findUserInDatabase(email)
    
    if len(result) < 0:
        # Nothing found
        return func.HttpResponse(json.dumps({
            "status": "fail",
            "message": "Given user was not found."
        }), mimetype="application/json")
    else:
        # Update entry to be logged in
        item = result[0]
        isLoggedIn = item["isLoggedIn"]
        return func.HttpResponse(json.dumps({
            "status": "success",
            "isLoggedIn": isLoggedIn
        }), mimetype="application/json")


