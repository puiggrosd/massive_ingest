# main.py

import json
import uuid
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import asyncpg
import pika
import time
import datetime
from bson import ObjectId
import os
import gridfs

mongodburl= os.getenv("MONGODB_URL", "mongodb://localhost:27017")
rabbitmq_host= os.getenv("RABBITMQ_HOST", "localhost")
from sqlalchemy.orm import sessionmaker
from models import JSONData, engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from models import init_db

from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = MongoClient(mongodburl)
    app.state.db = app.state.mongo_client["mydatabase"]
    app.state.collection = app.state.db["documents"]

    app.state.rabbitmq_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, heartbeat=0)  # Set heartbeat interval to 60 seconds
    )
    app.state.rabbitmq_channel = app.state.rabbitmq_connection.channel()
    app.state.rabbitmq_channel.queue_declare(queue='data_queue')
    app.state.rabbitmq_channel.queue_declare(queue='image_queue')
    init_db()
    yield
    app.state.mongo_client.close()
    await app.state.postgres_pool.close()
    app.state.rabbitmq_connection.close()

app = FastAPI(lifespan=lifespan)

from pydantic import BaseModel
class DataModel(BaseModel):
    name: str
    description: str

@app.post("/store_data")
async def store_data(data: str = Form(...)):
    data_dict = json.loads(data)
    uuid_str = str(uuid.uuid4())
    data_dict["uuid"] = uuid_str
    data_dict["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Send JSON data to RabbitMQ
    app.state.rabbitmq_channel.basic_publish(
        exchange='',
        routing_key='data_queue',
        body=json.dumps(data_dict),  # we can remove the image
        properties=pika.BasicProperties(
            headers={"uuid": uuid_str}
        )
    )
    
    # Send file data to RabbitMQ
    app.state.rabbitmq_channel.basic_publish(
        exchange='',
        routing_key='image_queue',
        body=json.dumps(data_dict),  # we can remove all the data that are not the image
        properties=pika.BasicProperties(
            headers={"uuid": uuid_str}
        )
    )
    app.state.collection.insert_one(data_dict)
    return JSONResponse(status_code=200, content={"message": "Data stored successfully"})

@app.get("/stats")
async def stats():
    # Get total count and last 10 documents
    total_count = app.state.collection.count_documents({})
    last_10 = list(app.state.collection.find().sort("timestamp", -1).limit(10))

    # Convert ObjectId to string for JSON serialization
    last_10 = [{k: v for k, v in doc.items() if not k.startswith('_')} for doc in last_10]

    return {"total_count": total_count, "last_10": last_10}

@app.get("/stats-postgres")
async def stats_postgres():
    db = SessionLocal()
    try:
        # Get total count and last 10 documents
        total_count = db.query(JSONData).count()
        last_10 = db.query(JSONData).order_by(JSONData.timestamp.desc()).limit(10).all()
        return {"total_count": total_count, "last_10": [data.__dict__ for data in last_10]}
    finally:
        db.close()