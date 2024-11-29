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

# the _accumulate functions, take the discrepancy accumulated on the inner cells so far as a parameter. improves execution time for the _interior_distance and _total_distance functions
def define_accumulate_interior_distance(func, normalized=True):
  def calculate_distance(nCell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values):    
    if nCell > 0 :
      new_discrepancy = (abs(initial_values[cell_id] - new_values[cell_id]))
      inner_discrepancy = func([inner_discrepancy*(nCell-1), new_discrepancy] )
    nCell= max(nCell,1)
    if normalized:
      inner_discrepancy = inner_discrepancy/nCell
    return inner_discrepancy
  return calculate_distance

def define_accumulate_margin_distance(func, normalized=True):
  def calculate_distance(nCell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values):    
    discrepancies = [0]
    nCell= max(nCell,1)
    for id in new_constraint_values:
      discrepancies.append(abs(initial_constraint_values[id] - new_constraint_values[id])) 
    result = func(discrepancies)
    if normalized:
      result = result/nCell
    return result
  return calculate_distance  

def define_accumulate_total_distance(normalized=True): 
  calculate_margin_distance    = define_accumulate_margin_distance(sum, normalized=normalized)
  accumulate_interior_distance = define_accumulate_interior_distance(sum, normalized=normalized)
  
  def calculate_total_distance(nCell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values):
    margin_distance = calculate_margin_distance(nCell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values) 
    inner_distance  = accumulate_interior_distance(nCell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values)
    total_distance  = margin_distance + inner_distance
    return [total_distance, margin_distance, inner_distance]
  
  return calculate_total_distance
