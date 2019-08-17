import json

class database_manager:

    def __init__(self):
        pass


    # Code for requesting data

    def request_events(self, zipcode: str):
        ''' Return list of events associated with specified zipcode '''
        events = []

        # Open the file with the name zipcode and load the json object
        with open(zipcode, "r") as json_file:
            json_object = json.load(json_file)

        # Add each event to events list
        for event in json_object.keys():
            events.append(event)

        return events

        

    def request_messages(self, zipcode: str, event: str):
        ''' Return list of messages associated with the zipcode and event '''
        # Open the file with the name zipcode and load the json object
        with open(zipcode, "r") as json_file:
            json_object = json.load(json_file)

        # Return messages list from specific event
        return json_object[event]


    # Code for updating the database

    def add_zipcode(self):
        pass

    def add_event(self, zipcode: str, event: str):
        ''' Adds specified event to zipcode location '''
        with open(zipcode, "r") as json_file:
            json_object = json.load(json_file)

        json_object[event] = []

    def add_message(self, zipcode: str, event: str, message: str):
        with open(zipcode, "r") as json_file:
            json_object = json.load(json_file)

        json_object[event].append(message)
