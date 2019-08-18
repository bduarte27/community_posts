import socket

server_ip = socket.gethostbyname(socket.gethostname())
public_ip = '71.204.145.90'
port = 8000

def run_client():
    global socket
    
    client_socket = socket.socket()

    # username required from client
    username = input("What is your username?: ")

    # connect client to server
    client_socket.connect((server_ip, port))

    # make recv and send calls non blocking for client
    client_socket.setblocking(0)

    client_socket.send(username.encode('utf-8'))

    while True:
        recieve_message(client_socket)
        post_message(client_socket, username)


def recieve_message(client_socket: socket.socket):
    ''' Prints out messages posted from other clients '''
    # recv will raise BlockingIOError if there is nothing to recieve
    try:
        print(client_socket.recv(1024).decode('utf-8'))
    except BlockingIOError:
        pass


def post_message(client_socket: socket.socket, username: str):
    ''' Sends message to other clients '''
    user_input = input(f"{username} (Press Enter to refresh and 'EMPTY' to close): ")

    if user_input == "":
        pass
    elif user_input == "EMPTY":
        print(f"Closing Connection for {username}!")
        client_socket.close()
        print("Connection Closed!")
    else: 
        # send will return an exception if it blocks
        client_socket.send(user_input.encode('utf-8'))


if __name__ == '__main__':
    run_client()
