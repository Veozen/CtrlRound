#all distance functions must acces input parameters partial_solution, initial_values, constraints, constraint_values

def define_interior_distance(func, normalized=True):
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

def define_margin_distance(func, normalized=True):
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

def define_total_distance(normalized=True): 
  calculate_margin_distance   = define_margin_distance(sum, normalized=normalized)
  calculate_interior_distance = define_interior_distance(sum, normalized=normalized)
  
  def calculate_total_distance(nCell, initial_values, new_values, initial_constraint_values, new_constraint_values):
    return calculate_margin_distance(nCell, initial_values, new_values, initial_constraint_values, new_constraint_values) + calculate_interior_distance(nCell, initial_values, new_values, initial_constraint_values, new_constraint_values)
  
  return calculate_total_distance
