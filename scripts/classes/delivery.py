
from datetime import date

import json

class Delivery():
    def __init__(self, order_id, delivery_date):
        self.__order_id = order_id
        self.__delivery_date = delivery_date

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Delivery):
            return self.__order_id == other.__order_id and self.__delivery_date == other.__delivery_date
        return False

    # Getters

    def get_order_id(self):
        return self.__order_id

    def get_delivery_date(self):
        return self.__delivery_date

    # JSON related functions

    def __getstate__(self) -> str:
        return {
            "order_id": self.__order_id,
            "delivery_date": self.__delivery_date.isoformat()
        }
    
    def __setstate__(self, object_dict):
        self.__order_id = object_dict['order_id']
        self.__delivery_date = date.fromisoformat(object_dict['delivery_date'])
    
    def to_json_string(self):
        return self.__getstate__()

    @classmethod
    def from_json_string(cls, json_string):
        obj = cls(None, None)
        obj.__setstate__(json_string)
        return obj

    def export_to_json_file(self, output_file):
        with open(output_file, 'w') as outfile:
            outfile.write(json.dumps(self.to_json_string(), sort_keys=False, indent=4))

    @classmethod
    def read_from_json_file(cls, input_json_file):
        with open(input_json_file) as json_file:
            return Delivery.from_json_string(json.load(json_file))
