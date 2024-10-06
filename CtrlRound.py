import pandas as pd
import heapq
import distance
from best_first_search import best_first_search


def CtrlRound(df_in, by, margins, var, roundingBase=1):
"""
input:
  df_in       :
  by          :
  margins     :
  var         :
  roudingBase :
"""
  
  by_to_cellId = {}
  initial_values = {}
  possible_cell_values = { }
  constraints = { }
  constraint_values = { }

  
  result = best_first_search(possible_cell_values, initial_values, constraints, constraint_values, NSolutions = 1)
  df_out = pd.DataFrame(result)
  return df_out
