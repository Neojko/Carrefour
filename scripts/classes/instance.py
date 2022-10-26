
import json

from classes.order import Order

class Instance():
    def __init__(self, orders):
        self.__orders = orders

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Instance):
            return self.__orders == other.__orders
        return False

    # Getters

    def get_orders(self):
        return self.__orders

    def get_earliest_delivery_date(self):
        return min([x.get_earliest_delivery_date() for x in self.__orders])


    # JSON related functions

    def __getstate__(self) -> str:
        return {
            "orders": [order.to_json_string() for order in self.__orders]
        }

    def __setstate__(self, object_dict):
        self.__orders = [Order.from_json_string(x) for x in object_dict['orders']]
    
    def to_json_string(self):
        return self.__getstate__()
    
    @classmethod
    def from_json_string(cls, json_string):
        obj = cls(None)
        obj.__setstate__(json_string)
        return obj

    def export_to_json_file(self, output_file):
        with open(output_file, 'w') as outfile:
            outfile.write(json.dumps(self.to_json_string(), sort_keys=False, indent=4))

    @classmethod
    def read_from_json_file(cls, input_json_file):
        with open(input_json_file) as json_file:
            return Instance.from_json_string(json.load(json_file))
