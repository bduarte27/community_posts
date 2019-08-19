import socket
import select
import json

server_ip = socket.gethostbyname(socket.gethostname())
public_ip = '71.204.145.90'
port = 8000

'''
Client will be in 1 of 3 modes
- zipcode mode:
    will enter zipcode location
- event mode:
    can request existing events, create new event, enter an event messaging catalogue, or return to zipcode mode
- message mode:
    can send messages or return to event mode
'''

def run_client():
    global socket
    running = True

    client_info = {'username': '', 'zipcode': '', 'event': ''}
    
    client_socket = socket.socket()

    # username required from client
    client_info['username'] = input("What is your username?: ")

    # connect client to server
    client_socket.connect((server_ip, port))

    client_socket.send(client_info['username'].encode('utf-8'))

    while running:
        if client_info['zipcode'] == '':
            zipcode_mode(client_info, client_socket)
        if client_info['zipcode'] != '' and client_info['event'] == '':
            event_mode(client_socket, client_info)
        if client_info['zipcode'] != '' and client_info['event'] != '':
            messaging_mode(client_socket, client_info)


def zipcode_mode(client_info, client_socket):
    ''' Update client_info to have specified zipcode '''
    client_info['zipcode'] = input("What is your zipcode?: ")
    client_socket.send(f"{client_info['zipcode']} GOTO".encode('utf-8'))
    #print(client_socket.recv(1024).decode('utf-8'))

    
def event_mode(client_socket: socket.socket, client_info):
    ''' Apply one of the specified options described below: ALL, POST, GET, BACK '''
    print("ALL: to request all events")
    print("POST event_name: where event_name is the name of the event to create a new event post")
    print("GET event_name: where event_name is the name of the event to enter the event_name messaging catalogue")
    print("BACK: to change location\n")
    while True:
        response = input("Enter your option here: ")

        if response == 'ALL':
            # send request for events to server
            client_socket.send(f"{client_info['zipcode']} {response}".encode('utf-8'))

            # print list of events to client -> event_list size will vary, need make repetitive reads later
            all_events = client_socket.recv(1024).decode('utf-8')
            print(json.loads(all_events))

        elif response[:4] == 'POST':
            # post new event to server at zipcode location
            client_socket.send(f"{client_info['zipcode']} {response}".encode('utf-8'))
            print(client_socket.recv(1024).decode('utf-8'))

        elif response[:3] == 'GET':
            # client will now move to messaging mode
            client_info['event'] = response[4:]
            break

        elif response == 'BACK':
            # client will now move back to zipcode mode
            client_info['zipcode'] = ''
            break


def messaging_mode(client_socket: socket.socket, client_info):
    """ 
    1.) keep client updated with messages
    2.) allow client to send messages OR return to event mode
    """
    # send request for messages from specified event
    client_socket.send(f"{client_info['zipcode']} GET {client_info['event']}".encode('utf-8'))
    all_messages = client_socket.recv(1024).decode('utf-8')
    print("\n",all_messages, "\n")

    if all_messages == "NO_EVENT":
        print("Going back to event mode!\n")
        client_info['event'] = ''
        return

    print(f"Welcome to the {client_info['event']} event message board")
    print('Type BACK to return to event mode any time')
    # Print out all messages from specified event catalogue -> message_list size will vary, need make repetitive reads later

    while True:
        response = input('Enter your message: ')
        
        if response == 'BACK':
            # client will now move back to event mode
            client_info['event'] = ''
            break
        
        # client must wait till server returns message_list
        client_socket.send(f"{client_info['zipcode']} {client_info['event']} {response}".encode('utf-8'))

        _recieve_data_nonblocking(client_socket)



def _recieve_data_nonblocking(client_socket: socket.socket):
    ''' Returns data requested from server '''
    client_socket.setblocking(0)

    # recv will raise BlockingIOError if there is nothing to recieve
    try:
        return client_socket.recv(1024).decode('utf-8')
    except BlockingIOError:
        pass

    client_socket.setblocking(1)



if __name__ == '__main__':
    run_client()
