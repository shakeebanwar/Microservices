from django.http import HttpResponse
import pika
import json

def publisher(request):
    message = {"email":"shakeebanwar250@gmail.com","subject":"Login Success","message":"Email send successfully"}
    # Convert the payload dictionary to a JSON string
    message = json.dumps(message)
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('localhost', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='my_queue1')
    channel.basic_publish(exchange='', routing_key='my_queue1', body=message)
    connection.close()
    return HttpResponse("Django publisher")