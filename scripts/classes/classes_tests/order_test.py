
from datetime import date

import unittest
import os

from classes.order import Order

class TestOrder(unittest.TestCase):

    def setUp(self) -> None:
        self.order_id = 'order_id'
        self.dict_delivery_date_to_cost = {
            date(2022, 10, 24): 13, 
            date(2023, 11, 25): 12
        }
        self.order = Order(order_id=self.order_id, dict_delivery_date_to_cost=self.dict_delivery_date_to_cost)

    def test_get_order_id(self):
        self.assertEqual(self.order_id, self.order.get_order_id())

    def test_get_dict_delivery_date_to_cost(self):
        self.assertEqual(self.dict_delivery_date_to_cost, self.order.get_dict_delivery_date_to_cost())

    def test_get_latest_delivery_date(self):
        self.assertEqual(date(2023, 11, 25), self.order.get_latest_delivery_date())

    def test_json_conversion_eq(self):
        json_string: str = self.order.to_json_string()
        new_order: Order = Order.from_json_string(json_string)
        self.assertEqual(new_order, self.order)

    def test_json_file_conversion_eq(self):
        file_path = 'here.json'
        self.order.export_to_json_file(file_path)
        new_order = Order.read_from_json_file(file_path)
        self.assertEqual(self.order, new_order)
        os.remove(file_path)
    
if __name__ == '__main__':
    unittest.main()
