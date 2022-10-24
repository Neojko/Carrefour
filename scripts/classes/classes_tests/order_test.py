
from datetime import date

import unittest
import os

from scripts.classes.order import Order

class TestOrder(unittest.TestCase):

    def setUp(self) -> None:
        self.order_id = 'order_id'
        self.delivery_dates = [date(2022, 10, 24), date(2023, 11, 25)]
        self.order = Order(order_id=self.order_id, delivery_dates=self.delivery_dates)

    def test_get_order_id(self):
        self.assertEqual(self.order_id, self.order.get_order_id())

    def test_get_delivery_dates(self):
        self.assertEqual(self.delivery_dates, self.order.get_delivery_dates())

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
