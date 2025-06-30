#sistema de mensajes con el usuario (choose your own story, single-player rpg) bueno, ya no
#main (producer recibe tareas del usuario)
import pika
import uuid
import json
import os

rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue='message_queue', durable=True)

response = None
correlation_id = str(uuid.uuid4())

def on_response(ch, method, props, body):
    global response
    if props.correlation_id == correlation_id:
        response = body.decode()

# Cola de respuesta especial de RabbitMQ
result = channel.queue_declare('', exclusive=True)
callback_queue = result.method.queue

channel.basic_consume(
    queue=callback_queue,
    on_message_callback=on_response,
    auto_ack=True
)

message_text = input("Ingresa tu mensaje (máximo 500 caracteres): ")
data = {
    'task_id': correlation_id,
    'message': message_text
}

channel.basic_publish(
    exchange='',
    routing_key='message_queue',
    body=json.dumps(data),
    properties=pika.BasicProperties(
        reply_to=callback_queue,
        correlation_id=correlation_id,
        delivery_mode=2
    )
)

print(" [x] Mensaje enviado. Esperando respuesta...")

# Esperar respuesta del consumidor
while response is None:
    connection.process_data_events()

print(f" [✓] Respuesta recibida: {response}")
connection.close()



