import socket
import select

server_ip = socket.gethostbyname(socket.gethostname())
public_ip = '71.204.145.90'
port = 8000

def client_run():
    global socket
    
    client_socket = socket.socket()

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
            x = input(f"{Username} press Enter to see comment and 'CLOSE <Username>"
                      +" to close connection: ")
            if x == '':
                continue
            elif x.upper() == "CLOSE {Username}":
                print(f"Closing connection for {Username}!" )
                client_socket.close()
                print(f"Connection Closed!")
                break
            else: 
                write_socket[0].send(x.encode('utf-8'))




if __name__ == '__main__':
    client_run()
