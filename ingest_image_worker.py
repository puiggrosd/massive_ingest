# image_worker.py

import base64
import json
import pika
import os
import uuid
rabbitmq_host= os.getenv("RABBITMQ_HOST", "localhost")

def image_callback(ch, method, properties, body):
    message = body.decode('utf-8')
    data = json.loads(message)
    image_data = base64.b64decode(data["image"])
    message = properties.headers
    uuid_str = message['uuid']
    folder_1 = uuid_str[:4]
    folder_2 = uuid_str[4:8]
    filename = f"{uuid_str}.jpg"
    save_path = os.path.join('./image_data', folder_1, folder_2)
    os.makedirs(save_path, exist_ok=True)
    with open(os.path.join(save_path, filename), "wb") as f:
        f.write(image_data)
    print(f" [x] Saved image data to {save_path}/{filename}: {data['uuid']}")

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()

channel.queue_declare(queue='image_queue')

channel.basic_consume(queue='image_queue', on_message_callback=image_callback, auto_ack=True)

print(' [*] Waiting for image messages. To exit press CTRL+C')
channel.start_consuming()
