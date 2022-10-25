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
        self.__order_and_deliveries_df = self.create_dataframe_of_possible_delivery_dates_per_order()
        self.build_problem_sets()
        self.create_problem_variables()
        self.create_problem_constraints()
        self.create_problem_objective()


    def create_dataframe_of_possible_delivery_dates_per_order(self):
        df = pd.DataFrame([
            (
                order,
                order.get_order_id(),
                delivery_date,
                cost
             )
            for order in self.__instance.get_orders()
            for delivery_date, cost in order.get_dict_delivery_date_to_cost().items()
        ], columns=['ORDER', 'ORDER_ID', 'DELIVERY_DATE', 'COST'])

        df['DELIVERY_DATE_INT'] = df['DELIVERY_DATE'].apply(lambda x: self.get_delivery_date_int(x))
        df['WEEK_DAY_INT'] = df['DELIVERY_DATE'].apply(lambda x: x.weekday())
        return df


    def get_delivery_date_int(self, delivery_date: date) -> int:
        return (delivery_date - self.__earliest_date).days


    def build_problem_sets(self):
        """Build sets to index the model variables."""
        # Set of order IDs
        self.__model.O = pyomo.Set(initialize=self.__order_and_deliveries_df['ORDER_ID'].unique())

        # Set of week days
        self.__model.W = pyomo.Set(initialize=range(7))

        # Index of the y variables: set of (order_id, delivery_date_id) assignments
        self.__model.Y = pyomo.Set(
            initialize=[tuple(x) for x in
                        self.__order_and_deliveries_df[['ORDER_ID', 'DELIVERY_DATE_INT']].drop_duplicates().values])


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


    def create_constraint_c1(self):
        """Create constraint to ensure that all orders are delivered once"""
        for order_id in self.__model.O:
            self.__model.constraints.add(self.get_Y_tuples_for_order_id(order_id)== 1)
    

    def get_Y_tuples_for_order_id(self, given_order_id: str):
        """Returns all (order_id, delivery_date_int) tuples in self.__model.Y such that order_id == given_order_id"""
        return sum([self.__model.y[o, d] for o, d in self.__model.Y if o == given_order_id])


    def create_problem_objective(self):
        self.__model.objective = pyomo.Objective(expr=self.__model.z_plus+self.get_Y_tuples(),sense=pyomo.minimize)

    
    def get_Y_tuples(self):
        """Returns all (order_id, delivery_date_int) tuples in self.__model.Y"""
        return sum([self.__model.y[o, d] for o, d in self.__model.Y])


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


if __name__ == '__main__':
    # Read data
    instance = Instance.read_from_json_file(config.INPUT_INSTANCE_PATH)

    # Run Solver
    solver = Solver(instance)
    results = solver.solve()

    # Get Solution
    # Print KPIs
    # Run the result though the Validator
    # Save Solution
    a = 3
