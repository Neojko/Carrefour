'''
Config file for the MILP solver.
'''

MINUTE_IN_SECONDS = 60
HOUR_IN_SECONDS = 3600

# I/O Locations
INPUT_INSTANCE_PATH = 'data/instance_10_7_100.json'
OUTPUT_SOLUTION_PATH = 'results/solution_10_7_100.json'
MILP_SOLVER_LOG_FILE = 'log/solution_10_7_100.log'

# Solver parameters
PRINT_SOLVER_OUTPUT = False
TIME_LIMIT = 1 * MINUTE_IN_SECONDS
GAP = 0.01
