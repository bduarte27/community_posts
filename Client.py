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
            user_input = input(f"{Username} (Press Enter to refresh and 'EMPTY' to close): ")

            if user_input == "":
                continue
            elif user_input == "EMPTY":
                print(f"Closing Connection for {Username}!")
                client_socket.close()
                print("Connection Closed!")
                break
            else: 
                write_socket[0].send(user_input.encode('utf-8'))

if __name__ == '__main__':
    client_run()
