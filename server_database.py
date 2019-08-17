import json

DB_Path = '.\DB'

class database_manager:

    def __init__(self):
        pass


    # Code for requesting data

    def request_events(self):
        pass

    def request_messages(self):
        pass


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

        self._open_data(file_path, json_object)

        json_object[event] = []

        self._dump_data(file_path, json_object)

        
    def add_message(self, zip_code: str, event: str, message: str) -> None:
        ''' Add Message in the json Database '''
        file_path = f".\DB\{zip_code}.json"
        json_object = dict()
        
        self._open_data(file_path, json_object)

        json_object[event].append(message)

        self._dump_data(file_path, json_object)


    def _open_data(self, file_path: str, json_dict: dict) -> None:
        with open(file_path, "r") as json_file:
            json_dict = json.load(json_file)
        


    def _dump_data(self, file_path: str, data: dict) -> None:
        ''' Dump data to json file '''
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)




x = database_manager()
x.add_zipcode("94533")
x.add_event("94533", "Fight")
x.add_message("94533", "Fight", "Hello")
