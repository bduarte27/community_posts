import socket
import select
import server_database

# server location
SERVER_IP = socket.gethostbyname(socket.gethostname())
PUBLIC_IP = '71.204.145.90'
SERVER_PORT = 8000
db = server_database.Database_Manager()


def run_server():
    global socket
    
    # create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_init(server_socket)

    # list of all sockets: server + clients
    socket_list = [server_socket]

    # Key = client socket object, Value = (Username, Zipcode)
    client_data = {}

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
                clientInfo_recv(client_socket, client_data, socket_list)
                
            else:
                try:
                    message = read_socket.recv(1024).decode('utf-8')
                    if len(message) == 0:
                        close_clientLine(read_socket, socket_list, client_data)
                        continue
                    print(clientCommands_RCVed(message, client_data, read_socket))

                    
                except ConnectionResetError:
                    close_clientLine(read_socket, socket_list, client_data)
                    continue

        
##        for write_socket in write_sockets:
##            client_zipCode = client_data[write_socket][1]
##            all_events = db.request_events(client_zipCode)
##            msg = f"\nFrom Client->"
            

def clientCommands_RCVed(client_command: "Client Input", client_data: "Client Dictionary",
                         read_socket: "Client's Socket") -> str:
    ''' '''
    message_data = client_command.split()
    
    if message_data[1] == "ALL":
        # Create a message for all possible Commands
        return get_ALLEvents(message_data[0])
    elif message_data[1] == "POST":
        print(message_data)
        return post_Event(message_data[0], message_data[2])
    
    else:
        # Message System -> User has to attached to a zipcode and event in order to send message to the system
        pass



def get_ALLEvents(zip_code: str) -> str:
    ''' get all Events as str and return as msg '''
    allEvents = db.request_events(zip_code)
    print(allEvents)
    msg = "".join(f"\n{i+1}.) {allEvents[i]}\n" for i in range(len(allEvents)))
    return msg


def post_Event(zip_code: str, event_name: str) -> str:
    ''' Post Event on the DB -> Creating a meessage of completion '''
    try:
        db.add_event(zip_code, event_name)
        return f"{event_name} Added in {zip_code}!"
    except server_database.ObjectAlreadyExist:
        return f"{event_name} in {zip_code}... Already Exist!"
        

def clientInfo_recv(client_socket: "Client's socket connection", client_data: 'Client Dictionary',
                    socket_list: "List of Sockets") -> None:
    ''' Server Receives client information and add it to its connection '''
    user_data = client_socket.recv(1024).decode('utf-8')
    user_name = user_data
    socket_list.append(client_socket)
    client_data[client_socket] = user_name
    

def close_clientLine(client_socket: "Client's socket", socket_list: 'list of socket',
                     client_dictionary: 'dictionary of users'):
    ''' Close the connection to the client and delete user_data info '''
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
