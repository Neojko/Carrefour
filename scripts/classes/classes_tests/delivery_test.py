
from datetime import date

import unittest
import os

from scripts.classes.delivery import Delivery

class TestDelivery(unittest.TestCase):

    def setUp(self) -> None:
        self.order_id = 'order_id'
        self.delivery_date = date(2022, 10, 24)
        self.delivery = Delivery(order_id=self.order_id, delivery_date=self.delivery_date)

    def test_get_order_id(self):
        self.assertEqual(self.order_id, self.delivery.get_order_id())

    def test_get_delivery_date(self):
        self.assertEqual(self.delivery_date, self.delivery.get_delivery_date())

    def test_json_conversion_eq(self):
        json_string: str = self.delivery.to_json_string()
        new_delivery: Delivery = Delivery.from_json_string(json_string)
        self.assertEqual(new_delivery, self.delivery)

    def test_json_file_conversion_eq(self):
        file_path = 'here.json'
        self.delivery.export_to_json_file(file_path)
        new_delivery = Delivery.read_from_json_file(file_path)
        self.assertEqual(self.delivery, new_delivery)
        os.remove(file_path)
    
if __name__ == '__main__':
    unittest.main()
