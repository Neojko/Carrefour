
import json

from scripts.classes.delivery import Delivery

class Solution():
    def __init__(self, deliveries):
        self.__deliveries = deliveries

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Solution):
            return self.__deliveries == other.__deliveries
        return False

    # Getters

    def get_deliveries(self):
        return self.__deliveries

    # JSON related functions

    def __getstate__(self) -> str:
        return {
            "deliveries": [delivery.to_json_string() for delivery in self.__deliveries]
        }

    def __setstate__(self, object_dict):
        self.__deliveries = [Delivery.from_json_string(x) for x in object_dict['deliveries']]
    
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
            return Solution.from_json_string(json.load(json_file))
