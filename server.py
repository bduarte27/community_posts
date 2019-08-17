import socket
import select
import pickle

# server location
SERVER_IP = socket.gethostbyname(socket.gethostname())
PUBLIC_IP = '71.204.145.90'
SERVER_PORT = 8000


debug = False

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

    # Key = client username, Value = latest client message
    client_messages = {}

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
                client_messages[username_data] = ""
                socket_list.append(client_socket)

            # recieve client messages
            else:
                
                if debug:
                    print("\nTesting the proccess of the connection------\n")
                    print("Usernames: ", client_dictionary.values(), f"<- Accessing {client_dictionary[read_socket]}")
                    print("Current Connection: ", client_dictionary[read_socket])

                try:
                    message = read_socket.recv(1024)
                    message = message.decode('utf-8')

                    if len(message) == 0:
                        close_clientLine(read_socket, socket_list, client_dictionary, client_messages)
                        continue
                    
                    if debug:
                        print(client_dictionary[read_socket] + ": " + message)
                    client_messages[client_dictionary[read_socket]] = message
                    
                except ConnectionResetError:
                    close_clientLine(read_socket, socket_list, client_dictionary, client_messages)
                    continue
                    

        for each_user in client_messages:
            for write_socket in write_sockets:
                if write_socket in socket_list and each_user != client_dictionary[write_socket] and client_messages[each_user] != "":
                    msg = f"\nFrom Client -> {each_user}: {client_messages[each_user]}\n"
                    # This line causes a bug on disconnecting to a server!
                    write_socket.send(msg.encode("utf-8"))
            client_messages[each_user] = ""


def close_clientLine(client_socket: "Client's socket", socket_list: 'list of socket',
                     client_dictionary: 'dictionary of users', client_messages: 'dictionary of messages'):
    ''' '''
    print(f"Closing the socket for -> {client_dictionary[client_socket]}")
    socket_list.remove(client_socket)
    # For now wer are also deleting the messages for testing purposes

    if debug:
        print("\nTesting the Closure of the connection------\n")
        print("Usernames: ", client_dictionary.values(), f"<- Removing {client_dictionary[client_socket]}")                    

    del client_messages[client_dictionary[client_socket]]
    del client_dictionary[client_socket]
    print("Connection closed!")
    


if __name__=='__main__':
    run_server()
