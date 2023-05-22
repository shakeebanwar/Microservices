
import threading
from fastapi import FastAPI
import pika
import uvicorn
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "consumer"}

def send_email(email: str, subject: str, message: str):
    # Email configurations
    sender_email = "appointments@virtualtriage.ca"
    sender_password = "123virtualtriage123"
    smtp_server = "smtpout.secureserver.net"
    smtp_port = 587

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    # Add message body
    msg.attach(MIMEText(message, "plain"))

    try:
        # Create a secure SSL/TLS connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}


def consume_messages():
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('localhost', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='my_queue1')

    def callback(ch, method, properties, body):
        data = eval(body.decode())
        send_email(data["email"],data["subject"],data["message"])
        print("Received message:",eval(body.decode())["email"])


    

    channel.basic_consume(queue='my_queue1', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Create a separate thread for message consumption
consumer_thread = threading.Thread(target=consume_messages, daemon=True)
consumer_thread.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)
