#recibe tares del producer y las ejecuta siguiendo su lógica
import pika
import json
import os
from database import save_message, get_total_messages

def process_message(data):
    message = data['message']
    if len(message) > 500:
        return "rechazado"
    return "recibido"

def callback(ch, method, properties, body):
    data = json.loads(body)
    task_id = data['task_id']
    message = data['message']

    print(f"[x] Procesando mensaje {task_id}")

    status = process_message(data)
    save_message(task_id, message, status)

    print(f"[✓] Resultado: {status.upper()} - enviado a reply_to")

    # Responder al productor si se especificó reply_to
    if properties.reply_to:
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=status.encode(),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
            )
        )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, body):
    data = json.loads(body)
    task_id = data['task_id']
    message = data['message']

    print(f"[x] Procesando mensaje {task_id}")

    status = process_message(data)
    save_message(task_id, message, status)

    total = get_total_messages()
    notification = ""

    if total % 5 == 0:
        notification = "5X5"
        print(f"[5] Felicidades! {notification}")

    # Construir respuesta para el productor
    response_msg = status
    if notification:
        response_msg += f" - {notification}"

    # Enviar respuesta si se especificó reply_to
    if properties.reply_to:
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=response_msg.encode(),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
            )
        )

    ch.basic_ack(delivery_tag=method.delivery_tag)


rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue='message_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='message_queue', on_message_callback=callback)

print('[*] Esperando mensajes. Presiona CTRL+C para salir')
channel.start_consuming()



