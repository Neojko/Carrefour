
from datetime import date

import json

class Order():
    def __init__(self, order_id, delivery_dates):
        self.__order_id = order_id
        self.__delivery_dates = delivery_dates

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Order):
            return self.__order_id == other.__order_id and self.__delivery_dates == other.__delivery_dates
        return False

    # Getters

    def get_order_id(self):
        return self.__order_id

    def get_delivery_dates(self):
        return self.__delivery_dates

    # JSON related functions

    def __getstate__(self) -> str:
        return {
            "order_id": self.__order_id,
            "delivery_dates": [delivery_date.isoformat() for delivery_date in self.__delivery_dates]
        }
    
    def __setstate__(self, object_dict):
        self.__order_id = object_dict['order_id']
        self.__delivery_dates = [date.fromisoformat(x) for x in object_dict['delivery_dates']]
    
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
            return Order.from_json_string(json.load(json_file))
