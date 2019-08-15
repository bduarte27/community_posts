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
    socket_inputs = [server_socket]
    socket_outputs = []

    # server starts looking for connections
    server_socket.listen()

    print("Server running!")
    print(f"Server IP: {SERVER_IP} PUBLIC IP: {PUBLIC_IP} SERVER PORT: {SERVER_PORT}")
    
    # keep server running
    client_dictionary = {}
    
    while True:    
        # read_sockets = sockets with data to read from
        # write_sockets = sockets ready for writing to
        # exception_sockets = sockets with error response
        read_sockets, write_sockets, exception_sockets = select.select(socket_inputs, socket_outputs, socket_inputs)

        # respond to sockets with recieved data
        for socket in read_sockets:
            # accept and save new connections
            if socket == server_socket:
                client_socket, client_address = server_socket.accept()
                socket_inputs.append(client_socket)
            else:
                if socket not in client_dictionary:
                    user_data = socket.recv(1024).decode()
                    client_dictionary[socket] = user_data
                    print(client_dictionary)



 
            
    server_socket.close()
            
        

if __name__=='__main__':
    run_server()
