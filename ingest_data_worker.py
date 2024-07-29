
import pika
import json
import uuid as uuid_lib
from sqlalchemy.orm import sessionmaker
from models import JSONData, engine
from datetime import datetime, timezone
import os
import logging
rabbitmq_host= os.getenv("RABBITMQ_HOST", "localhost")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def json_callback(ch, method, properties, body):
    message = body.decode('utf-8')
    data = json.loads(message)
    db = SessionLocal()
    try:
        new_data = JSONData(
            uuid=data['uuid'],
            name=data['name'],
            description=data['description'],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        db.add(new_data)
        db.commit()
    finally:
        db.close()
    print(f" [x] Stored JSON data: {data['uuid']}")

logging.error(f"{rabbitmq_host=}")
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()

channel.queue_declare(queue='data_queue')

channel.basic_consume(queue='data_queue', on_message_callback=json_callback, auto_ack=True)

print(' [*] Waiting for JSON messages. To exit press CTRL+C')
channel.start_consuming()