
def define_margin_distance(func, normalized=True):  
  #define the distance function used through the aggregation function used on the margins
  def calculate_margin_distance(partial_solution, initial_values, constraints, constraint_values):
      # merge the solution so far with initial values for the cells where no decision has been taken yet
      current_values = initial_values.copy()
      for cell,val in partial_solution.items():
          current_values[cell]=val
          
      nCell = len(partial_solution)        
      marginDiscrepancies = []
      for cons in constraints:
        target_value = constraint_values[cons]
        current_value = sum(current_values[cell_id] for cell_id in constraints[cons])
        marginDiscrepancies.append(abs(target_value - current_value))  
      if nCell >1 and normalized:
        return func(marginDiscrepancies)/nCell
      else:
        return func(marginDiscrepancies)
  return calculate_margin_distance

def define_margin_distance_(func, normalized=True):  
  #define the distance function used through the aggregation function used on the margins
  def calculate_margin_distance(partial_solution, initial_values, cell_id_constraints, constraint_values):
      nCell = len(partial_solution) 
      margin_discrepancies    = []
      all_cons_to_be_adjusted = set([cons_id for cell_id in partial_solution for cons_id in cell_id_constraints[cell_id]])
      margin_values           = {cons_id: constraint_values[cons_id] for cons_id in all_cons_to_be_adjusted }
      
      #adjust the margins
      for cell_id in partial_solution:
        for cons_id in cell_id_constraints[cell_id]:
          margin_values[cons_id] +=  partial_solution[cell_id] - initial_values[cell_id]
          
      for cons_id in margin_values:
        initial_value   = constraint_values[cons_id]
        current_value   = margin_values[cons_id]
        margin_discrepancies.append(abs(current_value - initial_value)) 
        
      if nCell> 1 and normalized:
        return func(margin_discrepancies)/nCell
      else:
        return func(margin_discrepancies) 

  return calculate_margin_distance
  
def define_interior_distance(func, normalized=True): 
  #define a distance function on the interior cells
  def calculate_interior_distance(partial_solution, initial_values, constraints, constraint_values):
      # calculate the deviation from the origianl values in the interior cells
      # constraints and constraints values are not used but are input parameter to have a uniform interface across all distance functions
      if len(partial_solution) == 0 :
        return 0
      nCell = len(partial_solution) 
      if nCell >1 and normalized:
        return func(abs(partial_solution[cell] - initial_values[cell]) for cell in partial_solution)/nCell
      else:
        return func(abs(partial_solution[cell] - initial_values[cell]) for cell in partial_solution)
      
  return calculate_interior_distance


def define_total_distance(normalized=True): 
  calculate_margin_distance   = define_interior_distance(sum, normalized=normalized)
  calculate_interior_distance = define_margin_distance(sum, normalized=normalized)
  
  def calculate_total_distance(partial_solution, initial_values, constraints, constraint_values):
    return calculate_margin_distance(partial_solution, initial_values, constraints, constraint_values) + calculate_interior_distance(partial_solution, initial_values, constraints, constraint_values)
  
  return calculate_total_distance


#-----------------------

def modify_margins(cell_id, previous_value, new_value, constraints_list, constraint_values):
  new_constraint_values = constraint_values.copy()
  for cons in constraints_list:
    new_constraint_values[cons] = new_constraint_values[cons]-previous_value + new_value
  return new_constraint_values

def define_distance(func, normalized=True):
  def calculate_distance(nCell, initial_values, new_values):    
    discrepancies = [0]
    nCell= max(nCell,1)
    for id in new_values:
      discrepancies.append(abs(initial_values[id] - new_values[id])) 
    result = func(discrepancies)
    if normalized:
      result = result/nCell
    return result
  return calculate_distance

def define_inner_distance_(func, normalized=True):
  def calculate_distance(nCell, initial_values, new_values, initial_constraint_values, new_constraint_values):    
    discrepancies = [0]
    nCell= max(nCell,1)
    for id in new_values:
      discrepancies.append(abs(initial_values[id] - new_values[id])) 
    result = func(discrepancies)
    if normalized:
      result = result/nCell
    return result
  return calculate_distance

def define_contraints_distance_(func, normalized=True):
  def calculate_distance(nCell, initial_values, new_values, initial_constraint_values, new_constraint_values):    
    discrepancies = [0]
    nCell= max(nCell,1)
    for id in new_constraint_values:
      discrepancies.append(abs(initial_constraint_values[id] - new_constraint_values[id])) 
    result = func(discrepancies)
    if normalized:
      result = result/nCell
    return result
  return calculate_distance  

def define_total_distance_(normalized=True): 
  calculate_margin_distance   = define_contraints_distance_(sum, normalized=normalized)
  calculate_interior_distance = define_inner_distance_(sum, normalized=normalized)
  
  def calculate_total_distance(partial_solution, initial_values, constraints, constraint_values):
    return calculate_margin_distance(partial_solution, initial_values, constraints, constraint_values) + calculate_interior_distance(partial_solution, initial_values, constraints, constraint_values)
  
  return calculate_total_distance
  
