
from classes.order import Order
from classes.instance import Instance

import create_random_instance_config as config

from datetime import date, timedelta
import random

class RandomInstanceCreator():
    def __init__(self):
        random.seed(config.RANDOM_SEED)
        self.__delivery_gap_range : list = range(1, config.RANGE_OF_DELIVERY_DATES+1)

    def create_instance(self) -> Instance:
        next_order_date: date = date.fromisoformat(config.STARTING_DAY)
        orders: list[Order] = []
        while len(orders) != config.NUMBER_OF_ORDERS:
            order_id = len(orders) + 1
            order = self.__create_order(order_id, next_order_date)
            orders.append(order)
            next_order_date = self.__compute_next_order_date(order)
        return Instance(orders)

    def __create_order(self, order_id, order_date) -> Order:
        delivery_dates: list[str] = self.__get_order_delivery_dates(order_date)
        date_to_cost: dict = {delivery_date: self.__compute_random_cost() for delivery_date in delivery_dates}
        return Order(order_id, date_to_cost)

    def __get_order_delivery_dates(self, current_date: date):
        day_gaps = random.sample(self.__delivery_gap_range, config.NUMBER_OF_DELIVERY_DATES_PER_ORDER)
        day_gaps.sort()
        return [(current_date + timedelta(days=day)) for day in day_gaps]

    def __compute_random_cost(self):
        return random.randint(config.MIN_COST, config.MAX_COST)

    def __compute_random_gap(self):
        return random.randint(config.MIN_GAP_BETWEEN_LAST_DELIVERY_DAY_AND_NEXT_ORDER, \
            config.MAX_GAP_BETWEEN_LAST_DELIVERY_DAY_AND_NEXT_ORDER)

    def __compute_next_order_date(self, last_order: Order):
        return last_order.get_latest_delivery_date() + timedelta(days=self.__compute_random_gap())


if __name__ == '__main__':
    instance_creator = RandomInstanceCreator()
    instance = instance_creator.create_instance()
    instance.export_to_json_file(config.OUTPUT_FILE_NAME)
