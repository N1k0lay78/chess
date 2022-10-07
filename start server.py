from socket import socket
from test_server.server_new import Server

self_ip = socket.gethostbyname(socket.gethostname())

print(self_ip)

server = Server(self_ip)
print(server.create_game())