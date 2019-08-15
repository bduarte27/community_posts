import socket
import select
import pickle

# server location
SERVER_IP = socket.gethostbyname(socket.gethostname())
PUBLIC_IP = '71.204.145.90'
SERVER_PORT = 8000

def run_server():
    global socket
    
    # create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # setup server socket settings
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # list of all sockets: server + clients
    socket_list = [server_socket]

    # server starts looking for connections
    server_socket.listen()

    print("Server running!")
    print(f"Server IP: {SERVER_IP} PUBLIC IP: {PUBLIC_IP} SERVER PORT: {SERVER_PORT}")

    # Key = client socket object, Value = client address tuple
    client_dictionary = {}
    
    # keep server running
    while True:
        # read_sockets = sockets with data to read from
        # write_sockets = sockets ready for writing to
        # exception_sockets = sockets with error response
        read_sockets, write_sockets, exception_sockets = select.select(socket_list, socket_list, socket_list)

        # respond to sockets with recieved data
        for read_socket in read_sockets:
            # accept and save new connections to socket_list and client_dictionary
            if read_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                # Get the user_name data from the client
                username_data = client_socket.recv(1024).decode('utf-8')
            
                client_dictionary[client_socket] = username_data
                socket_list.append(client_socket)

            # recieve client messages
            else:
                message = read_socket.recv(1024)

                # Remove and close the socket if client closed their connection
                if len(message) == 0:
                    print(f"Closing the socket for -> {client_dictionary[read_socket]}")
                    socket_list.remove(read_socket)
                    del client_dictionary[read_socket]
                    read_socket.close()
                    print("Connection closed!")
                    continue

                # Print and save message
                message = message.decode('utf-8')
                print(client_dictionary[read_socket] + ": " + message)


if __name__=='__main__':
    run_server()
