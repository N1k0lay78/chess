import socket
from core.online.Server import Server

# self_ip = socket.gethostbyname(socket.gethostname())

print('85.193.92.74')

server = Server('85.193.92.74', 8080)
print(server.create_game())