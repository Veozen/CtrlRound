## Description  
Controlled rounding is a technique used in data publishing to ensure that data released for public use meets specific confidentiality requirements. 
The process adjusts the data values by rounding them to a predetermined base in a such a way that the margins of the resulting table remain closer to their original values than they would should the table's entries have been simply rounded to their nearest base.  

Here the solution to this problem is found by applying a best-first-search method where the decision is to round up or down each non-margin entry.  

## Usage  

### ctrl_round(df_in, by, var, margins, rounding_base, fix_rounding_dist, max_heap_size):
Aggregates a dataframe and perform controlled rounding of it's entries.  

### Input
- **df_in**             : pandas DataFrame
- **by**                : list of column names on which to aggregate the input DataFrame
- **margins**           : list of lists of column names indicating which grouping to aggregate. Can be empty, in which case all grouping and subgrouping are aggregated. Controlling the rounding on a subset of margins will improve the run-time but will leave the other margins free to potentially deviate far from their original values.
- **var**               : column to be aggregated
- **rounding_base**     : the rounding base. Has to be greater than 0.
- **fix_rounding_dist** : if an entry is close to a rounded value by p% of the rounding base, round that entry to its closest rounded value and remove the other rounded value from consideration for that entry. This reduces the search space and run time at the cost of the quality of the solution.
- **max_heap_size**     : the maximum size of the heap. Has to be greater than 2. Default is 1000. A smaller heap will lead to faster run-time at the cost of the quality of the solution.

### Output
A dictionary with the following keys:
- **input_table**     : the original input data with columns listed in the "by" and "var" input parameters.
- **input_margins**   :
- **rounded_table**   : the rounded solution of input data with columns listed in the "by" and "var" input parameters.
- **rounded_margins** :
- **objectives**      : the objective function's value for the solution
- **opt_report**      : a dictionary containing information about the optimisation process with the following keys:
  - **n_iterations**  : the number of partial solutions expanded
  - **n_heap_purges** : the number of times the heap was purged, keeping the best solution so far
  - **n_sol_purged**  : the total number of partial solutions that got purged and never further expanded
  - **n_cells**       : the number of entries in the input table
  - **n_margins**     : the number of margin values from the input table
  - **n_fixed_cells** : the number of cells where the rounding is fixed and not subject to the optimisation process

