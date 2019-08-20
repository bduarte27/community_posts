import json
from pathlib import Path

class EventAlreadyExist(Exception):
    pass

class Database_Manager:
    # Code for requesting data

    def request_events(self, zip_code: str) -> [str]:
        ''' Return list of events associated with specified zipcode '''
        file_path = Path("DB") / Path(f"{zip_code}.json")
        events = []

        json_object = self._load_data(file_path)

        # Add each event to events list
        for event in json_object.keys():
            events.append(event)

        return events


    def request_messages(self, zip_code: str, event: str, number_of_messages: int) -> [str]:
        ''' Return list of messages associated with the zipcode and event '''
        try:
            file_path = Path("DB") / Path(f"{zip_code}.json")
            json_object = self._load_data(file_path)
            return json_object[event][number_of_messages:]
        except KeyError:
            raise KeyError

            
    # Code for updating the database

    def add_zipcode(self, zip_code: str) -> None:
        ''' Add Zipcode in the json Database '''
        file_path = Path("DB") / Path(f"{zip_code}.json")
        try:
            with open(file_path, "r") as json_file:
                return
        except FileNotFoundError:
            self._dump_data(file_path, {})
            
            
    def add_event(self, zip_code: str, event: str) -> None:
        ''' Add Event in the json Database '''
        file_path = Path("DB") / Path(f"{zip_code}.json")

        json_object = self._load_data(file_path)

        if event not in json_object:
            json_object[event] = []
            self._dump_data(file_path, json_object)
        else:
            raise EventAlreadyExist()
        

        
    def add_message(self, zip_code: str, event: str, message_info: tuple) -> None:
        ''' Add message_info of format [message, time] to json Database '''
        file_path = Path("DB") / Path(f"{zip_code}.json")
        json_object = self._load_data(file_path)

        i = len(json_object[event])
        for stored_message_info in reversed(json_object[event]):
            if stored_message_info[1] <= message_info[1]:
                break
            i -= 1

        json_object[event].insert(i, message_info)

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
    x = Database_Manager()
    x.add_zipcode("94532")
    x.add_event("94532", "Testing")
    x.add_message("94532", "Testing", "WTF!")
