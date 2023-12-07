import os
from typing import List
from fastapi import FastAPI, Body, Request
from fastapi.encoders import jsonable_encoder
import pymongo
from pydantic import BaseModel 
from bson.objectid import ObjectId 
import socket 
import time 
import random
import string

MONGO_DETAILS = os.getenv("DB_URL")
APP_NAME = os.getenv("APP_NAME")

if not MONGO_DETAILS:
    MONGO_DETAILS = "mongodb://admin:admin@mongodb:27017/"

if not APP_NAME:
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    APP_NAME = random_chars 

client = pymongo.MongoClient(MONGO_DETAILS)
db = client['myDatabase_C3'] 
collection = db['C_Tiga'] 

class Item(BaseModel):
    name: str
    age: int 
    favorite_game: str
    genre: List[str] = []
    playHours : int

def myData(data):
    return {
        "id": str(data["_id"]),
        "name": data["name"],
        "age": data["age"],
        "favorite_game": data["favorite_game"],
        "genre": data["genre"],
        "playHours": data["playHours"],
    }

def myFullData(datas):
    return [myData(data) for data in datas]
    
def ResponseModel(data, message = "Success"):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error, 
        "code": code, 
        "message": message
    }

app = FastAPI()


@app.get('/')
async def home():
    return {
        "message": "This is server " + APP_NAME,
        "hostname": socket.gethostname()}

@app.get('/fast')
async def fast():
    time.sleep(0.5)
    return {
        "message": "Hello world from server " + APP_NAME,
        "opt": "fast"}

@app.get('/slow')
async def slow():
    time.sleep(2)
    return {
        "message": "Hello world from server " + APP_NAME,
        "opt": "slow"}

@app.get("/all")
async def get_all_data():
    return ResponseModel(myFullData(collection.find()), "All Good")

@app.post("/create", response_model=Item)
async def create_data(item : Item):
    lister = jsonable_encoder(item)
    client.myDatabase_C3.C_Tiga.insert_one(lister)
    return lister

@app.get("/get/{id}")
async def get_data(id: str):
    Objinstance = ObjectId(id)
    data = collection.find_one({"_id": Objinstance})
    if data:
        return ResponseModel(myData(data), APP_NAME)
    else:
        return ErrorResponseModel("An error occurred.", 404, "Data doesn't exist.")
