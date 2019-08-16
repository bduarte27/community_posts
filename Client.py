import socket
import select

client_socket = socket.socket()

server_ip = socket.gethostbyname(socket.gethostname())
public_ip = '71.204.145.90'
port = 8000

Username = input("What is you username?: ")

client_socket.connect((server_ip, port))

socket_list = [client_socket]
client_socket.send(Username.encode('utf-8'))

while True:

    read_socket, write_socket, exception_socket = select.select(socket_list, socket_list, socket_list)


    if read_socket:
        print(read_socket[0].recv(1024).decode("utf-8"))
        continue

    if write_socket:
        x = input(f"{Username}: ")
        if x == '':
            client_socket.close()
            print("Connection is closed!")
            break
        else: 
            write_socket[0].send(x.encode('utf-8'))
