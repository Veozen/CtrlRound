import pandas as pd
from itertools import combinations
import distance
from best_first_search import best_first_search
from distance import define_margin_distance, define_interior_distance

def aggBy(df:pd.DataFrame, by, var, id):
    #aggregate a grouped dataframe
    if by is None or not by:
        sum_value = df[var].sum()
        contributing_rows = list(df[id])
        df_agg = pd.DataFrame({
            var: [sum_value],
            id: [contributing_rows]
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
        for i in range(0,len(by)):
            comb = combinations(by,i)
            subsets = subsets + [list(c) for c in comb]
    else:
        subsets=[[]]
        
    if margins is not None:
        subsets = [sub for sub in subsets if sub in margins]
        
    df_out = pd.DataFrame()
    for sub in subsets:
        subAgg = aggBy(df, by=sub, var=var, id=id)
        df_out = pd.concat([df_out,subAgg],ignore_index=True)
    return df_out  


def get_unique_col_name(df,base_name):
  # Generate a unique column name
  i = 1
  newName = base_name
  while newName in df.columns:
      newName = f"{base_name}_{i}"
      i += 1   
  return newName

def CtrlRound(df_in, by, var, margins=None, roundingBase=1):
  """
  Aggregate a dataframe and perform controlled rounding of it's entries.
  input:
    df_in       : pandas dataframe
    by          : list of column names on which to aggregate the input dataframe
    margins     : list of list of column name indicating which grouping to aggregate. Can be empty in which case all grouping and subgrouping are aggregated.
    var         : column to be aggregated
    roudingBase : the rounding base. Has to be greater than 0.
    
  output:
    dataframe with columns listed in the "by" and "var" input parameters.
  """
  # aggregate "var" by "by" columns in case there are duplicates in the input to make sure we have a table with signle entries per cell
  by_values   = df_in.groupby(by).sum(var).reset_index()
  # get a unique name not already present in the dataframe to store cell identifier
  cellIdName  = get_unique_col_name(by_values,"cellId")
  # create a unique identifer for each cell of the table
  by_values[cellIdName]     = range(len(by_values))
  
  # create a mapping of each cell identifer to each value from the table
  var_values                = by_values[[cellIdName,var]].copy()
  initial_values            = {}
  for index, row in var_values.iterrows():
    initial_values[row[cellIdName]]  = row[var]
  
  # create a mapping of each cell identifer to each possible rounded value 
  possible_values           = var_values
  lower_residual            = possible_values[var] % roundingBase
  lower  = get_unique_col_name(by_values,"lower")
  upper  = get_unique_col_name(by_values,"upper")
  
  possible_values[lower]  = possible_values[var] - lower_residual
  possible_values[upper]  = possible_values[lower]
  
  # check if the original value is not already rounded, in which case the upper value should be the same.
  possible_values[upper][lower_residual > 0] +=   roundingBase
  possible_cell_values              = {}
  for index, row in possible_values[[cellIdName,lower,upper]].iterrows():
    # if upper is the same as lower, generate only one possibility
    if row[lower] != row[upper]:
      possible_cell_values[row[cellIdName]]  = [row[lower],row[upper]]
    else:
      possible_cell_values[row[cellIdName]]  = [row[lower]]
  
  # get margins of the input table
  df_margins              = aggregate_and_list(by_values, by, var, margins, cellIdName)
  consIdName              = get_unique_col_name(df_margins,"consId")
  df_margins[consIdName]  = range(len(df_margins))
  
  # create a mapping of each margin identifer to each aggregated value 
  constraint_values           = {}
  for index, row in df_margins[[consIdName,var]].iterrows():
    constraint_values[row[consIdName]] = row[var]
  
  # create a mapping of each margin identifer to a list of each cell identifer adding up to it
  constraints           = {}
  for index, row in df_margins[[consIdName,cellIdName]].iterrows():
    constraints[row[consIdName]] = row[cellIdName]
  
  # define out distances measures
  calculate_margin_max_distance   = define_margin_distance(max)
  calculate_margin_sum_distance   = define_margin_distance(sum)
  calculate_interior_sum_distance = define_interior_distance(sum)
  distanceFuncs                   = [calculate_margin_max_distance, calculate_margin_sum_distance, calculate_interior_sum_distance]
  # obtain the best rounding
  result    = best_first_search(possible_cell_values, initial_values, constraints, constraint_values, distanceFuncs, NSolutions = 1)
  solution  = result[0][-1]
  objectives= result[0][:-1]
  # assign the rounded values into a dataframe ready for output
  df_out      = by_values.copy()
  
  df_out[var] = by_values[cellIdName].map(solution)
  margins     = aggregate_and_list(df_out, by, var, margins, cellIdName)
  margins     = margins[[*by,var]]
  df_out = df_out.drop(cellIdName,axis=1)
  
  return df_out, margins , objectives

