from datetime import datetime 
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

    client_info = {'username': '', 'zipcode': '', 'event': '', 'num_of_messages': 0}
    
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
    while True:
        zip_code = input("What is your zipcode?: ")
        if zip_code.strip() != "":
            client_info['zipcode'] = zip_code
            client_socket.send(f"{client_info['zipcode']} GOTO".encode('utf-8'))
            break

    
def event_mode(client_socket: socket.socket, client_info):
    ''' Apply one of the specified options described below: ALL, POST, GET, BACK '''
    print("\nALL: to request all events")
    print("POST event_name: where event_name is the name of the event to create a new event post")
    print("GET event_name: where event_name is the name of the event to enter the event_name messaging catalogue")
    print("BACK: to change location\n")
    while True:
        response = input("Enter your option here: ")

        if response == 'ALL':
            # send request for events to server
            client_socket.send(f"{client_info['zipcode']} {response}".encode('utf-8'))

            # print list of events to client -> event_list size will vary, need make repetitive reads later
            data = client_socket.recv(1024).decode('utf-8')
            allEvents = json.loads(data)
            pretty_print_all_messages(allEvents, "Events")
            
        elif response[:4] == 'POST':
            # post new event to server at zipcode location
            client_socket.send(f"{client_info['zipcode']} {response}".encode('utf-8'))
            print(client_socket.recv(1024).decode('utf-8'))

        elif response[:3] == 'GET':

            # send request for messages from specified event
            client_socket.send(f"{client_info['zipcode']} GET {response[4:]}".encode('utf-8'))
            data_str = client_socket.recv(1024).decode('utf-8')

            if data_str == "NO_EVENT":
                print(f"\nThis Event: '{response[4:]}' does not exist!")
                continue
            
            # client will now move to messaging mode
            client_info['event'] = response[4:]
            message_info_list = json.loads(data_str)
            client_info['num_of_messages'] = len(message_info_list)
            pretty_print_all_messages(message_info_list, "Messages")
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
    print(f"Welcome to the {client_info['event']} event message board")
    print('Type BACK to return to event mode any time\n')
    # Print out all messages from specified event catalogue -> message_list size will vary, need make repetitive reads later

    while True:
        response = input('Enter your message: ')
        
        if response == 'BACK':
            # client will now move back to event mode
            client_info['event'] = ''
            client_info['num_of_messages'] = 0
            break
        if response.strip() == "":
            continue
        
        utc_now = datetime.utcnow()
        utc_now_str = f"{utc_now}"
        message_info = [response, utc_now_str]

        # client sends user message and request to server to see if new messages present for this event at same time
        client_socket.send(f"{client_info['zipcode']} MESSAGES {client_info['event']} {client_info['num_of_messages']} {message_info}".encode('utf-8'))
        message_info_list = json.loads(client_socket.recv(1024).decode('utf-8'))      

        pretty_print_all_messages(message_info_list, "Messages")
        client_info['num_of_messages'] += len(message_info_list)


def pretty_print_all_messages(print_content: [], print_str: str):
    ''' prints print_content list in a nicer format '''
    print()
    if print_content == []:
        print(f"There are currently no available {print_str}!")
    else:
        print(f"Here are the available {print_str}: ")
        for i in print_content:
            print(i)
    print()


if __name__ == '__main__':
    run_client()
