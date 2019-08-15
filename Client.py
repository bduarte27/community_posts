import socket

client_socket = socket.socket()

server_ip = '192.168.0.110'
public_ip = '71.204.145.90'
port = 8000

Username = input("What is you username?: ")

client_socket.connect((public_ip, port))


while True:

    client_socket.send(Username.encode())


