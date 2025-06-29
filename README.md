# Mi Proyecto: Sistema de Mensajes con notificaciones

## Descripción
Una aplicación de mensajes basada en python que procesa en RabbitMQ y almacena mensajes y notificaciones específicas en base de datos en PostgreSQL

## Arquitectura
[ User ] --> [ Producer ] ---> [ Queu (RabbitMQ) ] ---> [ Consumer ]

    |                                          |
   └<-------- Respuesta --------(reply_to) <---┘


Base de datos

[ PostgreSQL ]
*   ├── Tabla messages-----------> Guarda todos los mensajes

   
 *  └── Tabla notifications------> Guarda logros como "5X5"

## Requisitos
- Docker
- Docker Compose
- pika
- psycopg2-binary


## Instrucciones
* Ingresar docker-compose up --build
* Una vez que corra, se envían mensajes desde python producer.py
en localhost:5672


## RepositorioSeminario
Seminario 2025
app_mensajes/
* ├── producer.py
* ├── consumer.py
* ├── db.py
* ├── requirements.txt
* ├── Dockerfile
* ├── docker-compose.yml
* └── init.sql


## Ejemplo de uso
* Productor: envía un mensaje de texto (ej. usuario escribe algo)
* Consumidor:
* 1) Valida que el mensaje no supere los 500 caracteres
* 2) Guarda el mensaje en PostgreSQL con estado recibido o rechazado
* 3) Retorna el estado por pnatalla


## Notas adicionales
- Implementar el programa Celery para el procesamiento de mensajes sería más eficiente
- El mensaje de retorno por pantalla podría implementarse por correo en futuras versiones
