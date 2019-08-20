from server_database import Database_Manager, EventAlreadyExist
import socket
import select
import json

# server location
SERVER_IP = socket.gethostbyname(socket.gethostname())
PUBLIC_IP = '71.204.145.90'
SERVER_PORT = 8000
db = Database_Manager()


def run_server():
    global socket
    
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

                    if len(client_request) == 0:
                        close_client(read_socket, socket_list, client_data)
                        continue

                    process_client_request(client_request, client_data, read_socket)
                    
                except ConnectionResetError:
                    close_client(read_socket, socket_list, client_data)
                    continue
                

def process_client_request(client_request: "request from client application", client_data: "Client Dictionary",
                         client_socket: "client socket"):
    ''' parse client request and decide on action to take '''
    request_data = client_request.split()
 
    if request_data[1] == "GOTO":
        db.add_zipcode(request_data[0])

    elif request_data[1] == "ALL":
        all_events = get_events(request_data[0])
        client_socket.send(all_events.encode('utf-8'))

    elif request_data[1] == "POST":
        notification = post_event(request_data[0], request_data[2])
        client_socket.send(notification.encode('utf-8'))

    elif request_data[1] == "GET":
        all_messages = get_messages(request_data[0], request_data[2], int(request_data[3]))
        client_socket.send(all_messages.encode('utf-8'))
        
    elif request_data[1] == "MESSAGES":
        message_list = request_data[4:]
        msg = " ".join(message_list)

        # add message to database
        db.add_message(request_data[0], request_data[2], msg)

        # send new messages back to client
        all_messages = get_messages(request_data[0], request_data[2], int(request_data[3]))
        client_socket.send(all_messages.encode('utf-8'))


def get_events(zip_code: str) -> str:
    ''' gather all events as a list and return as server_response '''
    event_list = db.request_events(zip_code)
    return json.dumps(event_list)


def post_event(zip_code: str, event_name: str) -> str:
    ''' post new event to database '''
    try:
        db.add_event(zip_code, event_name)
        return f"\n{event_name} Added in {zip_code}!\n"
    except EventAlreadyExist:
        return f"\n{event_name} in {zip_code}... Already Exist!\n"

def get_messages(zip_code: str, event: str, number_of_messages: int) -> str:
    try:
        msg_list = db.request_messages(zip_code, event, number_of_messages)
        return json.dumps(msg_list)
    except KeyError:
        return "NO_EVENT"


def server_recv_client(server_socket: socket.socket, client_data: 'client dictionary', socket_list: 'list of all sockets') -> None:
    ''' server accepts client connection and stores client information '''
    client_socket, client_address = server_socket.accept()
    user_data = client_socket.recv(1024).decode('utf-8')
    socket_list.append(client_socket)
    client_data[client_socket] = user_data
    

def close_client(client_socket: socket.socket, socket_list: 'list of all sockets',
                     client_data: 'client dictionary'):
    ''' close connection to client by removing from socket_list and client_dictionary '''
    print(f"Closing the socket for -> {client_data[client_socket]}")
    socket_list.remove(client_socket)
    del client_data[client_socket]
    print("Connection closed!")



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
