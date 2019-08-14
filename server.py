import socket
import select

# server location
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 2727

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

    # keep server running
    while True:
    
        # read_sockets = sockets with data to read from
        # write_sockets = sockets ready for writing to
        # exception_sockets = sockets with error response
        read_sockets, write_sockets, exception_sockets = select.select(socket_list, [], socket_list)

        # respond to sockets with recieved data
        for socket in read_sockets:

            # accept and save new connections
            if socket == server_socket:
                client_socket, client_address = server_socket.accept()

                socket_list.append(client_socket)

if __name__=='__main__':
    run_server()
