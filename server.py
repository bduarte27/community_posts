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


    ## Data Table for Testing Purposes
    client_dictionary = {}
    message_content = {}
    
    # keep server running
    while True:    
        # read_sockets = sockets with data to read from
        # write_sockets = sockets ready for writing to
        # exception_sockets = sockets with error response
        read_sockets, write_sockets, exception_sockets = select.select(socket_inputs, socket_outputs, socket_inputs)
        print(len(socket_outputs))
        # respond to sockets with recieved data
        for socket in read_sockets:
            # accept and save new connections
            if socket == server_socket:
                client_socket, client_address = server_socket.accept()
                socket_inputs.append(client_socket)
            else:
                socket_outputs.append(socket)
                # Checks if the user is already registered in the server if not then register
                if socket not in client_dictionary: 
                    user_data = socket.recv(1024).decode('utf-8')
                    client_dictionary[socket] = user_data

                    if _debugTRUE(1):
                        print(client_dictionary)

                # Else wait for the client's input for a data
                else:
                    # Receive and Decode the message given by the client
                    message = socket.recv(1024).decode('utf-8')
                    # Buggy, need to be replaced later (It Crashes the whole server)!
                    if message == '':
                        print(f"Closing the socket for -> {client_dictionary[socket]}")
                        # Remove the existing socket if the client closes the their connection
                        socket_inputs.remove(socket)
                        socket_outputs.remove(socket)
                        del client_dictionary[socket]
                        socket.close()
                        
                        if _debugTRUE(1):
                            print(len(socket_outputs))
                            print(client_dictionary)
                        print("Connection closed!")

                    else:
                        # Of the Message is not closed then the message will be printed in the server console and place a message on message_content (dictionary) (key: User, value: Message) 
                        print(client_dictionary[socket] + ": " + message)
                        message_content[client_dictionary[socket]] = message
                        
                        if _debugTRUE(1):
                            print("Dictonary Content")
                            for i in message_content:
                                print("Socket -> ", i, ": ", message_content[i])

        # Write to the clients of the server (Still Buggy)
        for socket in write_sockets:
            # Grab all the message currently stored in the message_content dictionary and send them to all the available client after their input
            for each_message in message_content: 
                message = "Client -> " + each_message + ": " + message_content[each_message] + "\n"
                socket.send(message.encode('utf-8'))
            # Remove the socket on the socket_outputs so that the message won't be repeatedly sent
            socket_outputs.remove(socket)
            
    server_socket.close()
            

def _debugTRUE(num: int) -> bool:
    return num == 1

if __name__=='__main__':
    run_server()
