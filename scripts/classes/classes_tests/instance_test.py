
from datetime import date

import unittest
import os

from scripts.classes.order import Order
from scripts.classes.instance import Instance

class TestInstance(unittest.TestCase):

    def setUp(self) -> None:
        self.first_order = Order(order_id='first', delivery_dates=[date(2022, 10, 24), date(2023, 11, 25)])
        self.second_order = Order(order_id='second', delivery_dates=[date(2021, 10, 24), date(2021, 11, 25)])
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
