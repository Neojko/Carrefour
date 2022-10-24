from scripts.classes.order import Order
from scripts.classes.instance import Instance
from scripts.classes.delivery import Delivery
from scripts.classes.solution import Solution

from scripts import milp_config


import pyomo.environ as pyomo
from datetime import date, datetime, timedelta


class Solver:

    def __init__(self, instance: Instance, milp_config: dict):
        self.__model = pyomo.ConcreteModel()
        self.build_decision_variable_helping_sets()
        self.create_problem_variables()
        self.create_problem_constraints()
        self.create_problem_objective()
        

    def build_decision_variable_helping_sets(self):
        """Build sets to index the model variables."""
        # TODO description
        a = 3

    def create_problem_variables(self):
        # TODO Description
        self.model.y = pyomo.Var(self.model.y_index, domain=pyomo.Binary, initialize=0)

    def create_problem_constraints(self):
        self.model.constraints = pyomo.ConstraintList()
        self.create_constraint_c1()

    def create_constraint_c1(self):
        """TODO to describe"""

    def create_problem_objective(self):
        self.model.objective = pyomo.Objective(expr=self.model.Z, sense=pyomo.minimize)

    def solve(self):
        solver = pyomo.SolverFactory('cbc')
        solver.options['PassF'] = 1
        solver.options['Heur'] = 'on'
        solver.options['ratioGap'] = milp_config['GAP']
        # solver.options['Cuts']='off'
        solver.options['zero'] = 'off'
        solver.options['gomory'] = 'off'
        # solver.options['strat']=2
        # solver.options['threads']=2
        print(f'MILP solver startedt at: {str(datetime.now())}')
        print(f'Time limit is set for {str(datetime.now() + timedelta(seconds=self.milp_config["TIME_LIMIT"]))}')
        results = solver.solve(
            self.model,
            tee=self.milp_config['PRINT_SOLVER_OUTPUT'],
            logfile=self.milp_config['MILP_SOLVER_LOG_FILE'],
            timelimit=self.milp_config['TIME_LIMIT']
        )
        return results


if __name__ == '__main__':
    # Read data
    instance = 3

    # Run Solver
    solver = Solver(instance, milp_config)
    results = solver.solve()

    # Get Solution
    # Print KPIs
    # Run the result though the Validator
    # Save Solution
    a = 3
