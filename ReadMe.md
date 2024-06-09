# Proyecto de Chat gRPC

## Descripción

Este proyecto implementa un sistema de chat utilizando gRPC, Redis y RabbitMQ. Permite a los usuarios iniciar sesión, conectarse entre sí, suscribirse a chats grupales, enviar mensajes y descubrir otros chats activos.

## Archivos Principales

- `chat.proto`: Define las estructuras de datos y los servicios gRPC utilizados en el proyecto.
- `server.py`: Implementa el servidor gRPC para manejar las solicitudes de chat.
- `name_server.py`: Gestiona la información de los usuarios y sus estados utilizando Redis.
- `client.py`: Implementa el cliente del chat que interactúa con el servidor gRPC y RabbitMQ.

## Proto

Para generar los archivos de Python a partir del archivo chat.proto, utiliza el siguiente comando:

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto

### Servidor

Para ejecutar el servidor, asegúrate de tener instalado gRPC y RabbitMQ. Luego, ejecuta el servidor con el siguiente comando:

python server.py

### Cliente

Para iniciar el cliente del chat, ejecuta el siguiente comando y sigue las instrucciones en pantalla:

python client.py


### Dependencias
    - gRPC
    - Redis
    - RabbitMQ
    - protobuf
Asegúrate de instalar las dependencias necesarias utilizando pip:

pip install grpcio grpcio-tools redis pika protobuf

-------------------ENGLISH---------------------------------

# gRPC Chat Project

## Description
This project implements a chat system using gRPC, Redis, and RabbitMQ. It allows users to log in, connect with each other, subscribe to group chats, send messages, and discover other active chats.

## Main Files
- `chat.proto`: Defines the data structures and gRPC services used in the project.
- `server.py`: Implements the gRPC server to handle chat requests.
- `name_server.py`: Manages user information and their states using Redis.
- `client.py`: Implements the chat client that interacts with the gRPC server and RabbitMQ.

## Proto
To generate the Python files from the chat.proto file, use the following command:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto

### Server
To run the server, make sure you have gRPC and RabbitMQ installed. Then, run the server with the following command:
python server.py

### Client
To start the chat client, run the following command and follow the on-screen instructions:
python client.py

## Dependencies
- gRPC
- Redis
- RabbitMQ
- protobuf

Make sure to install the necessary dependencies using pip:
pip install grpcio grpcio-tools redis pika protobuf


