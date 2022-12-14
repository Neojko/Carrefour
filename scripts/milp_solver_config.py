'''
Config file for the MILP solver.
'''

MINUTE_IN_SECONDS = 60
HOUR_IN_SECONDS = 3600

# Weights
WEIGHT_BALANCE = 1000
WEIGHT_COST = 1

# I/O Locations
INPUT_INSTANCE_PATH = 'data/instance_120000_7_100.json'
OUTPUT_SOLUTION_PATH = 'results/solution_120000_7_100.json'
MILP_SOLVER_LOG_FILE = 'log/solution_120000_7_100.log'

# Solver parameters
PRINT_SOLVER_OUTPUT = True
TIME_LIMIT = 5 * HOUR_IN_SECONDS
GAP = 0.05
