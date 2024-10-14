#all distance functions must acces input parameters partial_solution, initial_values, constraints, constraint_values

def define_margin_distance(func):  
  #define the distance function used through the aggregation function used on the margins
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
      return func(marginDiscrepancies)

  return calculate_margin_distance

def define_interior_distance(func): 
  #define a distance function on the interior cells
  def calculate_interior_distance(partial_solution, initial_values, constraints, constraint_values):
      # calculate the deviation from the origianl values in the interior cells
      # constraints and constraints values are not used but are input parameter to have a uniform interface across all distance functions
      if len(partial_solution) == 0 :
        return 0
      return func(abs(partial_solution[cell] - initial_values[cell]) for cell in partial_solution)
      
  return calculate_margin_distance
