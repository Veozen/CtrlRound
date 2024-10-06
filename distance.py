
def calculate_margin_distance(partial_solution, initial_values, constraints, constraint_values):
    # merge the solution so far with initial values for the cells where no decision has been taken yet
    current_values = {}
    for cell,val in initial_values.items():
      current_values[cell]=val
      if cell in partial_solution:
        current_values[cell]=partial_solution[cell]
            
    marginDiscrepancies = []
    for cons in constraints:
      target_value = constraint_values[cons]
      current_value = sum(current_values[cell_id] for cell_id in constraints[cons])
      marginDiscrepancies.append(abs(target_value - current_value))
    return sum(marginDiscrepancies)

def calculate_interior_distance(partial_solution, initial_values):
    if len(partial_solution) == 0 :
      return 0
    return sum(abs(partial_solution[cell] - initial_values[cell]) for cell in partial_solution)