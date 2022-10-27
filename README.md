This repository aims to solve a simplified MILP formulation of the Middle Mile problem.

Content:
- A scripts/create_random_instance.py script to create random instances
- A scripts/milp_solver.py to solve the MILP formulation on given instances
- Instances to solve in the data folder
- Some solutions (resp. logs) of previously solved instances in the solution (resp. log) folder

Requirements:
- Any Python version >= 3.7
- The pyomo package (tested with version 6.4.2)
- The CBC solver (brew install cbc should do the work on a Mac)
