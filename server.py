import socket
import select
import server_database

# server location
SERVER_IP = socket.gethostbyname(socket.gethostname())
PUBLIC_IP = '71.204.145.90'
SERVER_PORT = 8000


def run_server():
    global socket
    db = server_database.Database_Manager()
    
    # create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_init(server_socket)

    # list of all sockets: server + clients
    socket_list = [server_socket]

    # key = client socket, value = client username
    client_data = {}

    # keep server running
    while True:
        # read_sockets = sockets with data to read from
        # write_sockets = sockets ready for writing to
        # exception_sockets = sockets with error response
        read_sockets, write_sockets, exception_sockets = select.select(socket_list, socket_list, socket_list)

        # respond to sockets with recieved data
        for read_socket in read_sockets:
            # accept and save new connections to socket_list and client_data
            if read_socket == server_socket:
                server_recv_client(server_socket, client_data, socket_list)
                
            else:
                try:
                    client_request = read_socket.recv(1024).decode('utf-8')
                    # I don't think this is needed anymore with the current Client right now
                    if len(client_request) == 0:
                        close_client(read_socket, socket_list, client_data)
                        continue
                    print(process_client_request(client_request, client_data, read_socket))

                    
                except ConnectionResetError:
                    close_client(read_socket, socket_list, client_data)
                    continue

        
##        for write_socket in write_sockets:
##            client_zipCode = client_data[write_socket][1]
##            all_events = db.request_events(client_zipCode)
##            msg = f"\nFrom Client->"
            

def process_client_request(client_request: "request from client application", client_data: "Client Dictionary",
                         read_socket: "client socket") -> str:
    ''' parse client request and decide on action to take '''
    request_data = client_request.split()
    
    if request_data[1] == "ALL":
        return get_events(request_data[0])
    elif request_data[1] == "POST":
        return post_event(request_data[0], request_data[2])
    
    else:
        # Message System -> User has to attached to a zipcode and event in order to send message to the system
        pass



def get_events(zip_code: str) -> str:
    ''' gather all events as a list and return as server_response '''
    return db.request_events(zip_code)

def post_event(zip_code: str, event_name: str) -> str:
    ''' post new event to database '''
    try:
        db.add_event(zip_code, event_name)
        return f"\n{event_name} Added in {zip_code}!\n"
    except server_database.EventAlreadyExist:
        return f"\n{event_name} in {zip_code}... Already Exist!\n"
        

def server_recv_client(server_socket: socket.socket, client_data: 'client dictionary', socket_list: 'list of all sockets') -> None:
    ''' server accepts client connection and stores client information '''
    client_socket, client_address = server_socket.accept()
    user_data = client_socket.recv(1024).decode('utf-8')
    socket_list.append(client_socket)
    client_data[client_socket] = user_data
    

def close_client(client_socket: socket.socket, socket_list: 'list of all sockets',
                     client_data: 'client dictionary'):
    ''' close connection to client by removing from socket_list and client_dictionary '''
    print(f"Closing the socket for -> {client_dictionary[client_socket]}")
    socket_list.remove(client_socket)
    del client_dictionary[client_socket]
    print("Connection closed!")


def message_test(message_data: str, client_data) -> str:
    pass
    


def server_init(server_socket: 'Server Socket') -> None:
    ''' Initialize the connection to the Server '''
    print("Server Initializing...")
    # setup server socket settings
    server_socket.bind((SERVER_IP, SERVER_PORT))
    # server starts looking for connections
    server_socket.listen()
    print("Server Initialized!")
    print(f"Server IP: {SERVER_IP} PUBLIC IP: {PUBLIC_IP} SERVER PORT: {SERVER_PORT}")
    


if __name__=='__main__':
    run_server()
