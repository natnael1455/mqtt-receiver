import json
import logging
import os

import pymongo
from bson import json_util
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from lib.mongo_db import MongoDBConnection

# Configure logging settings
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load variables from .env file
load_dotenv()

app = FastAPI()


def get_data():
    try:
        mongo_uri = f"mongodb://{os.getenv('DB_host')}:{os.getenv('DB_port')}/"
        db_name = os.getenv("DB_name")
        collection_name = "data"
        connection = MongoDBConnection(mongo_uri, db_name)
        data = connection.get_documents(collection_name)
        connection.close_connection()  
        return data
    except pymongo.errors.ServerSelectionTimeoutError:
        logging.error("Connection to the database failed")
        raise HTTPException(
            status_code=404,
            detail=f"Connection to the database failed",
        )


@app.get("/")
def read_root():
    data = json.loads(json_util.dumps(get_data()))
    if len(data) == 0:
        raise HTTPException(
             status_code=404,
             detail=f"Items not found",
         )
    return JSONResponse(content=data)
    
