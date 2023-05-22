import os,uvicorn
from fastapi import FastAPI
import pika
from pydantic import BaseModel
import json

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "producer"}


class Item(BaseModel):
    email: str
    subject: str
    message: str

@app.post("/publish")
def publish_message(item: Item):
    message = {"email":item.email,"subject":item.subject,"message":item.message}
    # Convert the payload dictionary to a JSON string
    message = json.dumps(message)
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('localhost', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='my_queue1')
    channel.basic_publish(exchange='', routing_key='my_queue1', body=message)
    connection.close()
    return {"message": "Published successfully"}



if __name__ == '_main_':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)