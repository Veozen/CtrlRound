import pandas as pd
import heapq
import distance
from best_first_search import best_first_search


def CtrlRound(df_in, by, margins, var, roundingBase=1):
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
  
  by_to_cellId = {}
  initial_values = {}
  possible_cell_values = { }
  constraints = { }
  constraint_values = { }

  
  result = best_first_search(possible_cell_values, initial_values, constraints, constraint_values, NSolutions = 1)
  df_out = pd.DataFrame(result)
  return df_out
