from classes.order import Order
from classes.instance import Instance
from classes.delivery import Delivery
from classes.solution import Solution

import milp_solver_config as config

import pandas as pd
import pyomo.environ as pyomo
from datetime import date, datetime, timedelta


class Solver:

    def __init__(self, instance: Instance):
        self.__model = pyomo.ConcreteModel()
        self.__instance = instance
        self.__earliest_date = instance.get_earliest_delivery_date()
        self.__dict_int_to_week_day = self.build_dict_int_to_week_day()
        self.__dict_order_id_and_delivery_date_int_to_cost = self.build_dict_order_id_and_delivery_date_int_to_cost()
        self.build_problem_sets()
        self.create_problem_variables()
        self.create_problem_constraints()
        self.create_problem_objective()


    def get_delivery_date_int(self, delivery_date: date) -> int:
        return (delivery_date - self.__earliest_date).days

    
    def build_dict_int_to_week_day(self):
        return {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }


    def build_dict_order_id_and_delivery_date_int_to_cost(self):
        return {
            (order.get_order_id(), self.get_delivery_date_int(delivery_date)) : cost
            for order in self.__instance.get_orders()
            for delivery_date, cost in order.get_dict_delivery_date_to_cost().items()
        }


    def build_problem_sets(self):
        # Set of order IDs
        self.__model.O = pyomo.Set(initialize={order.get_order_id() for order in self.__instance.get_orders()})

        # Set of week days
        self.__model.W = pyomo.Set(initialize=range(7))

        # Index of the y variables: set of (order_id, delivery_date_id) assignments
        self.__model.Y = pyomo.Set(initialize=self.__dict_order_id_and_delivery_date_int_to_cost.keys())


    def create_problem_variables(self):
        # y[order, date] == 1 if order is delivered at date
        self.__model.y = pyomo.Var(self.__model.Y, domain=pyomo.Binary, initialize=0)

        # z[week_day] == X if X orders are delivered on week day week_day
        self.__model.z = pyomo.Var(self.__model.W, domain=pyomo.NonNegativeIntegers, initialize=0)

        # z_plus == X if biggest difference between any two z[week_day] variables == X
        self.__model.z_plus = pyomo.Var(domain=pyomo.NonNegativeIntegers, initialize=0)


    def create_problem_constraints(self):
        self.__model.constraints = pyomo.ConstraintList()
        self.create_constraint_c1()
        self.create_constraint_c2()
        self.create_constraint_c3()


    def create_constraint_c1(self):
        """Create constraint to ensure that all orders are delivered once"""
        for order_id in self.__model.O:
            self.__model.constraints.add(self.get_sum_of_Y_tuples_for_order_id(order_id)== 1)
    

    def get_sum_of_Y_tuples_for_order_id(self, order_id: str):
        return sum([self.__model.y[o, d] for o, d in self.__model.Y if o == order_id])


    def create_constraint_c2(self):
        """Create constraint to ensure relationship between y and z variables"""
        for week_day in self.__model.W:
            self.__model.constraints.add(self.get_sum_of_Y_tuples_for_week_day(week_day)== self.__model.z[week_day])

    
    def get_sum_of_Y_tuples_for_week_day(self, week_day):
        return sum([self.__model.y[o, d] for o, d in self.__model.Y if d%7 == week_day])


    def create_constraint_c3(self):
        """Create constraint to ensure relationship between z and z_plus variables"""
        for week_day1 in self.__model.W:
            for week_day2 in self.__model.W:
                if week_day1 != week_day2:
                    self.__model.constraints.add(self.__model.z_plus >= self.__model.z[week_day1] - self.__model.z[week_day2])


    def create_problem_objective(self):
        objective_function = config.WEIGHT_BALANCE * self.__model.z_plus + config.WEIGHT_COST * self.get_Y_tuples_times_cost()
        self.__model.objective = pyomo.Objective(expr=objective_function,sense=pyomo.minimize)

    
    def get_Y_tuples_times_cost(self):
        """Returns sum_{(o, d) in Y} y_{o,d} * cost_{o,d}"""
        return sum([self.__model.y[o, d] * self.__dict_order_id_and_delivery_date_int_to_cost[(o,d)] for o, d in self.__model.Y])


    def solve(self):
        solver = pyomo.SolverFactory('cbc')
        solver.options['ratioGap'] = config.GAP
        print(f'MILP solver started at: {str(datetime.now())}')
        print(f'Time limit is set for {str(datetime.now() + timedelta(seconds=config.TIME_LIMIT))}')
        results = solver.solve(
            self.__model,
            tee=config.PRINT_SOLVER_OUTPUT,
            logfile=config.MILP_SOLVER_LOG_FILE,
            timelimit=config.TIME_LIMIT
        )
        return results

    
    def build_solution(self) -> Solution:
        deliveries = []
        for (order_id, delivery_date_int) in self.__model.Y:
            if self.__model.y[(order_id, delivery_date_int)].value >= 1:
                x = type(delivery_date_int)
                delivery_date = self.__earliest_date + timedelta(days=int(delivery_date_int))
                deliveries.append(Delivery(int(order_id), delivery_date))
        return Solution(deliveries)


    def print_kpis(self):
        for week_day in self.__model.W:
            print("Number of deliveries on " + self.__dict_int_to_week_day[week_day] + ": " + str(self.__model.z[week_day].value))
        print("Max gap in deliveries between two week days: " + str(self.__model.z_plus.value))


if __name__ == '__main__':
    # Read data
    instance = Instance.read_from_json_file(config.INPUT_INSTANCE_PATH)

    # Run Solver
    solver = Solver(instance)
    results = solver.solve()

    # Get Solution
    solution = solver.build_solution()

    # Print KPIs
    solver.print_kpis()

    # Save Solution
    solution.export_to_json_file(config.OUTPUT_SOLUTION_PATH)
