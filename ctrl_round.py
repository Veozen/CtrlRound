import pandas as pd
from itertools import combinations
import functools
import time
import distance
from best_first_search import best_first_search
from distance import define_margin_distance, define_interior_distance
import pandas as pd
from itertools import combinations
import functools
import time
import distance
from best_first_search import best_first_search
from distance import define_margin_distance, define_interior_distance

def agg_by(df:pd.DataFrame, by, var, id):
    #aggregate a grouped dataframe
    if by is None or not by:
        sum_value = df[var].sum()
        contributing_rows = list(df[id])
        df_agg = pd.DataFrame({
            var: [sum_value],
            id : [contributing_rows]
        })
    else:
        df_agg = df.groupby(by).agg({
      var: "sum", 
      id: lambda x: x.tolist()
      }).reset_index()
    return df_agg

def aggregate_and_list(df:pd.DataFrame, by, var=None, margins=None, id=None):
    if by is not None and not isinstance(by,list):
        by = [by]
        
    subsets=[]
    if by is not None:
        for i in range(0, len(by)):
            comb = combinations(by, i)
            subsets = subsets + [list(c) for c in comb]
    else:
        subsets=[[]]
        
    if margins is not None:
        subsets = [sub for sub in subsets if sub in margins]
        
    df_out = pd.DataFrame()
    for sub in subsets:
        sub_agg = agg_by(df, by=sub, var=var, id=id)
        df_out = pd.concat([df_out,sub_agg], ignore_index=True)
    return df_out  


def get_unique_col_name(df, base_name):
  # Generate a unique column name
  i = 1
  new_name = base_name
  while new_name in df.columns:
      new_name = f"{base_name}_{i}"
      i += 1   
  return new_name

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer

@timer
def ctrl_round(df_in, by, var, margins=None, distance_max=False, distance_total=False, rounding_base=1, fix_rounding_dist= 0, max_heap_size= 1000, reset_heap_fraction=0.75):
  """
  Aggregate a dataframe and perform controlled rounding of it's entries.
  input:
    df_in             : pandas dataframe
    by                : list of column names on which to aggregate the input dataframe
    margins           : list of list of column name indicating which grouping to aggregate. Can be empty in which case all grouping and subgrouping are aggregated. 
    Controlling the rounding on a subset of margins will improve the run-time but will leave the other margins free to potentialy deviate far from their original values.
    var               : column to be aggregated
    rounding_base     : the rounding base. Has to be greater than 0.
    distance_max      : whether or not to include the maximum distance in the list of distances used to sort partial solutions. Not including it results in fewer partial solutions expanded and reduces the run-time.
    distance_total    : whether or not to add the distance on the margin with the distance on the interior cells as a sorting criterion. If True sorting will be done according to this sum instead of the margin sum then interior sum.
    fix_rounding_dist : if an entry is close to a rounded value by p% of the rounding base, round that entry to it's closest rounded value and remove the other rounded value from consideration for that entry. 
    This reduces the search space and run-time at the cost of the quality of the solution.
    max_heap_size     : the maximum size the heap. Has to be greater than 2. Default is 1000. 
    A smaller heap will lead to faster run-time at the cost of the quality of the solution.
    reset_heap_fraction: size of the heap after purging as a percentage of the maximum size. Default is 0.75
    
  output:
    A dictionary with following keys:
    input_table     : the original input data with columns listed in the "by" and "var" input parameters.
    input_margins   : the margins of the input table
    rounded_table   : the rounded solution of input data with columns listed in the "by" and "var" input parameters.
    rounded_margins : the margins of the rounded table
    objectives      : the objective functions value for the solution
    opt_report      : a dictionary containing information about the optimisation process with folowing keys:
      n_iterations  : the number of partial solution expanded
      n_heap_purges : the number of times the heap was purged, keeping the best solutions so far
      n_sol_purged  : the total number of partial solution that got purged and never further expanded
    n_cells         : the number of entries in the input table
    n_margins       : the number of margin values from the input table 
    n_fixed_cells   : the number of cells where the rounding is fixed and not subject to the optimisation process

  """
  
  # check input parameters
  if type(rounding_base) not in [int,float]:
    raise TypeError("rounding_base has to be integer or float")
    
  if type(max_heap_size) not in [int]:
    raise TypeError("max_heap_size has to be integer")
  
  if type(fix_rounding_dist) not in [int,float]:
    raise TypeError("fix_rounding_dist has to be integer or float")
    
  if type(reset_heap_fraction) not in [int,float]:
    raise TypeError("reset_heap_fraction has to be integer or float")
    
  if df_in.dtypes[var] not in [int,float] :
    raise TypeError(f"column '{var}' is must be of type int or float")
    
  if type(distance_max) is not bool:
    raise TypeError("distance_max has to be True or False")
    
  if type(distance_total) is not bool:
    raise TypeError("distance_total has to be True or False")
    
    
  if rounding_base <= 0:
    raise ValueError("rounding_base has to be greater than 0")
    
  if max_heap_size < 2:
    raise ValueError("max_heap_size has to be greater than 1")
    
  if fix_rounding_dist < 0:
    raise ValueError("fix_rounding_dist has to be greater than or equal to 0")
    
  if fix_rounding_dist >= 0.5:
    raise ValueError("fix_rounding_dist has to be less than 0.5")
  
  if reset_heap_fraction >= 1:
    raise ValueError("reset_heap_fraction has to be less than 1")
    
  if reset_heap_fraction < 0:
    raise ValueError("reset_heap_fraction has to be greater than 0")
    
  if var not in df_in.columns :
    raise KeyError(f"column '{var}' is not in input dataframe")
    
  for col in by:
    if col not in df_in.columns :
      raise KeyError(f"column '{col}' is not in input dataframe")
    
  
  n_cells       = 0
  n_margins     = 0
  n_fixed_cells = 0
  
  # aggregate "var" by "by" columns in case there are duplicates in the input to make sure we have a table with signle entries per cell
  by_values               = df_in.groupby(by).sum(var).reset_index()
  # get a unique name not already present in the dataframe to store cell identifier
  cell_id_name            = get_unique_col_name(by_values,"cellId")
  # create a unique identifer for each cell of the table
  by_values[cell_id_name] = range(len(by_values))
  cellId_lst              = list(by_values[cell_id_name])
  n_cells                 = len(cellId_lst)
  
  # create a mapping of each cell identifer to each value from the table
  var_values                = by_values[[cell_id_name,var]].copy()
  initial_values            = {}
  for index, row in var_values.iterrows():
    initial_values[row[cell_id_name]]  = row[var]
  
  # create a mapping of each cell identifer to each possible rounded value 
  possible_values = var_values
  lower_residual  = possible_values[var] % rounding_base
  lower           = get_unique_col_name(by_values,"lower")
  upper           = get_unique_col_name(by_values,"upper")
  residual        = get_unique_col_name(by_values,"residual")
  
  possible_values[lower]    = possible_values[var] - lower_residual
  possible_values[upper]    = possible_values[lower] + rounding_base
  possible_values[residual] = lower_residual
  
  
  # check if the original value is not already rounded, in which case the upper value should be the same.  
  possible_cell_values      = {cellId:[] for cellId in cellId_lst}
  for index, row in possible_values[[cell_id_name, lower, upper, residual]].iterrows():
    # if upper is the same as lower, generate only one possibility
    if row[residual] <= fix_rounding_dist * rounding_base:
      possible_cell_values[row[cell_id_name]]  = [row[lower]]
      n_fixed_cells += 1
    elif row[residual] > (1-fix_rounding_dist) * rounding_base:
      possible_cell_values[row[cell_id_name]]  = [row[upper]]
      n_fixed_cells += 1
    else:
      possible_cell_values[row[cell_id_name]]  = [row[lower], row[upper]]
      
  # get margins of the input table
  df_margins                = aggregate_and_list(by_values, by, var, margins, cell_id_name)
  cons_id_name              = get_unique_col_name(df_margins,"consId")
  df_margins[cons_id_name]  = range(len(df_margins))
  n_margins                 = len(df_margins)
  
  # create a mapping of each margin identifer to each aggregated value 
  constraint_values           = {}
  for index, row in df_margins[[cons_id_name, var]].iterrows():
    constraint_values[row[cons_id_name]] = row[var]
  
  # create a mapping of each margin identifer to a list of each cell identifer adding up to it
  constraints           = {}
  for index, row in df_margins[[cons_id_name,cell_id_name]].iterrows():
    constraints[row[cons_id_name]] = row[cell_id_name]
  
  # define out distances measures
  calculate_margin_max_distance   = define_margin_distance(max, normalized=False)
  calculate_margin_sum_distance   = define_margin_distance(sum)
  calculate_interior_sum_distance = define_interior_distance(sum)
  calculate_total_distance        = define_total_distance()
  if distance_total: 
    distanceFuncs                   = [calculate_total_distance]
  else:
    distanceFuncs                   = [calculate_margin_sum_distance, calculate_interior_sum_distance]
  if distance_max: 
    distanceFuncs                   = [calculate_margin_max_distance] + distanceFuncs
  else:
    distanceFuncs                   = distanceFuncs
  # obtain the best rounding
  result, n_iterations, n_heap_purges, n_sol_purged = best_first_search(possible_cell_values, initial_values, constraints, constraint_values, distanceFuncs, n_solutions = 1, max_heap_size= max_heap_size, reset_heap_fraction= reset_heap_fraction )
  solution    = result[0][-1]
  objectives  = result[0][:-1]
  # assign the rounded values into a dataframe ready for output
  df_out      = by_values.copy()
  df_out[var] = by_values[cell_id_name].map(solution)
  margins     = aggregate_and_list(df_out, by, var, margins, cell_id_name)
  margins     = margins[[*by,var]]
  
  #clean up the output
  df_out      = df_out.drop(cell_id_name,axis=1)
  by_values   = by_values.drop(cell_id_name,axis=1)
  df_margins  = df_margins.drop(cell_id_name,axis=1)
  df_margins  = df_margins.drop(cons_id_name,axis=1)
  
  #if the maximum distance was not used to sort partial solutions, provide that distance in the report anyway
  max_distance      = calculate_margin_max_distance(solution, initial_values, constraints, constraint_values)
  sum_distance      = calculate_margin_sum_distance(solution, initial_values, constraints, constraint_values)  
  interior_distance = calculate_interior_sum_distance(solution, initial_values, constraints, constraint_values) 
  objectives = (max_distance,sum_distance,interior_distance)
    
  # report information from the optimization process
  opt_report                  = {}
  opt_report["n_iterations"]  = n_iterations
  opt_report["n_heap_purges"] = n_heap_purges
  opt_report["n_sol_purged"]  = n_sol_purged
  
  output = {"input_table"     : by_values, \
            "input_margins"   : df_margins, \
            "rounded_table"   : df_out, \
            "rounded_margins" : margins, \
            "objectives"      : objectives, \
            "opt_report"      : opt_report, \
            "n_cells"         : n_cells, \
            "n_margins"       : n_margins, \
            "n_fixed_cells"   : n_fixed_cells}
            
  return output


