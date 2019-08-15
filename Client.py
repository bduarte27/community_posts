import socket

client_socket = socket.socket()

server_ip = '192.168.0.110'
public_ip = '71.204.145.90'
port = 8000

Username = input("What is you username?: ")

client_socket.connect((public_ip, port))
client_socket.send(Username.encode('utf-8'))

while True:

    x = input("Data to send? ")
    
    if x == '':
        client_socket.close()
        print("Connection is closed!")
        break
    else: 
        client_socket.send(x.encode('utf-8'))
