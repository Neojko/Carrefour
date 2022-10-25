
from datetime import date

import unittest
import os

from scripts.classes.order import Order
from scripts.classes.instance import Instance

class TestInstance(unittest.TestCase):

    def setUp(self) -> None:
        first_order_dict_delivery_date_to_cost = {
            date(2022, 10, 24).isoformat(): '13', 
            date(2023, 11, 25).isoformat(): '12'
        }
        second_order_dict_delivery_date_to_cost = {
            date(2022, 10, 26).isoformat(): '15', 
            date(2023, 11, 27).isoformat(): '16'
        }
        self.first_order = Order(order_id='first', dict_delivery_date_to_cost=first_order_dict_delivery_date_to_cost)
        self.second_order = Order(order_id='second', dict_delivery_date_to_cost=second_order_dict_delivery_date_to_cost)
        self.orders = [self.first_order, self.second_order]
        self.instance = Instance(orders=self.orders)

    def test_get_orders(self):
        self.assertEqual(self.orders, self.instance.get_orders())

    def test_json_conversion_eq(self):
        json_string: str = self.instance.to_json_string()
        new_instance: Instance = Instance.from_json_string(json_string)
        self.assertEqual(new_instance, self.instance)

    def test_json_file_conversion_eq(self):
        file_path = 'here.json'
        self.instance.export_to_json_file(file_path)
        new_instance = Instance.read_from_json_file(file_path)
        self.assertEqual(self.instance, new_instance)
        os.remove(file_path)
    
if __name__ == '__main__':
    unittest.main()
