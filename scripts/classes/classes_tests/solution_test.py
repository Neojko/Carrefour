
from datetime import date

import unittest
import os

from scripts.classes.delivery import Delivery
from scripts.classes.solution import Solution

class TestInstance(unittest.TestCase):

    def setUp(self) -> None:
        self.first_delivery = Delivery(order_id='first', delivery_date=date(2022, 10, 24))
        self.second_delivery = Delivery(order_id='second', delivery_date=date(2021, 10, 24))
        self.deliveries = [self.first_delivery, self.second_delivery]
        self.solution = Solution(deliveries=self.deliveries)

    def test_get_deliveries(self):
        self.assertEqual(self.deliveries, self.solution.get_deliveries())

    def test_json_conversion_eq(self):
        json_string: str = self.solution.to_json_string()
        new_solution: Solution = Solution.from_json_string(json_string)
        self.assertEqual(new_solution, self.solution)

    def test_json_file_conversion_eq(self):
        file_path = 'here.json'
        self.solution.export_to_json_file(file_path)
        new_solution = Solution.read_from_json_file(file_path)
        self.assertEqual(self.solution, new_solution)
        os.remove(file_path)
    
if __name__ == '__main__':
    unittest.main()
