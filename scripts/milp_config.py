'''
Config file for the MILP solver.
'''

from pickle import FALSE


MINUTE_IN_SECONDS = 60
HOUR_IN_SECONDS = 3600

milp_config = {
    # I/O Locations
    'INPUT_INSTANCE_PATH': 'ici',
    'OUTPUT_SOLUTION_PATH': 'ici',
    'MILP_SOLVER_LOG_FILE': 'ici',

    # I/O settings
    'DATE_JSON_FORMAT': '%Y-%m-%d',

    # Solver parameters
    'PRINT_SOLVER_OUTPUT': False,
    'TIME_LIMIT': 1 * MINUTE_IN_SECONDS,
    'GAP': 0.01
}

