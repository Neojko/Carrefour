
from datetime import date

import json

class Order():
    def __init__(self, order_id, dict_delivery_date_to_cost):
        self.__order_id: str = order_id
        self.__dict_delivery_date_to_cost: dict[date, int] = dict_delivery_date_to_cost

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Order):
            return self.__order_id == other.__order_id and \
                self.__dict_delivery_date_to_cost == other.__dict_delivery_date_to_cost
        return False

    # Getters

    def get_order_id(self) -> str:
        return self.__order_id

    def get_dict_delivery_date_to_cost(self):
        return self.__dict_delivery_date_to_cost

    def get_latest_delivery_date(self):
        return max(self.__dict_delivery_date_to_cost.keys())

    # JSON related functions

    def __getstate__(self) -> str:
        string_dict = { delivery_date.isoformat() : cost for delivery_date, cost in self.__dict_delivery_date_to_cost.items() }
        return {
            "order_id": self.__order_id,
            "delivery_dates": json.dumps(string_dict, sort_keys=False, indent=8)
        }
    
    def __setstate__(self, object_dict):
        self.__order_id = object_dict['order_id']
        string_dict = json.loads(object_dict['delivery_dates'])
        self.__dict_delivery_date_to_cost = {date.fromisoformat(key) : value for key, value in string_dict.items() }
    
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
