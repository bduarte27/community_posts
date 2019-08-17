import json

DB_Path = '.\DB'

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

    def add_zipcode(self, zip_code: str) -> None:
        ''' Add Zipcode in the json Database '''
        file_path = f".\DB\{zip_code}.json"
        try:
            with open(file_path, "r") as json_file:
                print("Already exist!")
                
        except FileNotFoundError:
            self._dump_data(file_path, {})
            
            
    def add_event(self, zip_code: str, event: str) -> None:
        ''' Add Event in the json Database '''
        file_path = f".\DB\{zip_code}.json"
        json_object = dict()

        json_object = self._load_data(file_path)

        json_object[event] = []

        self._dump_data(file_path, json_object)

        
    def add_message(self, zip_code: str, event: str, message: str) -> None:
        ''' Add Message in the json Database '''
        file_path = f".\DB\{zip_code}.json"
        json_object = dict()
        
        json_object = self._load_data(file_path)

        json_object[event].append(message)

        self._dump_data(file_path, json_object)


    def _load_data(self, file_path: str) -> dict:
        ''' Load data to json file and return dictionary '''
        with open(file_path, "r") as json_file:
            return json.load(json_file)


    def _dump_data(self, file_path: str, data: dict) -> None:
        ''' Dump data to json file '''
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)


if __name__ == '__main__':
    x = database_manager()
    x.add_zipcode("94532")
    x.add_event("94532", "Testing")
    x.add_message("94532", "Testing", "WTF!")
