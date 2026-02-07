## Description  
Controlled rounding is a technique used in data publishing to ensure that data released for public use meets specific confidentiality requirements. 
The process adjusts the data values by rounding them to a predetermined base in a such a way that the margins of the resulting table remain closer to their original values than they would should the table's entries have been simply rounded to their nearest base.  

Here the solution to this problem is found by applying a best-first-search method where the decision is to round up or down each non-margin entry. Four distance functions can used to sort partial solutions. 
- The max absolute difference between a margin's value and it's original value.  
- The sum of absolute difference between a margin's value and it's original value. 
- The sum of absolute difference between a table cell's rounded value and it's original value.  
- The sum of absolute difference between a both margin's value as well as table cell's rounded value and their original value.

The sum of absolute differences are divided by the number of cells rounded so far providing an average cost of the decision made so far. This distinction makes a difference when comparing partial solutions of different lengths.  
Ties on the first function are resolved by looking subsequent ones. The first complete solution found is returned. 

The distance functions can be used in various combinations depending on input parameters:
- sum on the margins, sum on the interior cells (Default)
- max on the margins, sum on the margins, sum on the interior cells (distance_max=true)
- sum on the margins + sum on the interior cells (distance_total=true)
- max on the margins, sum on the margins + sum on the interior cells  (distance_max=true and distance_total=true)

When a solution is returned, the first three distance functions are evaluated and written in the output along with the maximum discrepancy on the interior cells regardless of the combination of distance functions used in the search. Note that using the maximum on the margins distance function in the search seems to increase execution time.

If the input table contains multipule rows for the same "by" columns values, the table is grouped by the "by" columns and the "var" column is summed over.

## Usage 

**ctrl_round(df_in, by, var, margins, rounding_base, distance_max, distance_total, fix_rounding_dist, max_heap_size):**  
Aggregates a dataframe and perform controlled rounding of it's entries.  

**input:**  
- **df_in**             : pandas DataFrame of the interior cells of the table to be rounded
- **by**                : list of column names on which to aggregate the input DataFrame
- **margins**           : list of lists of column names indicating which grouping to aggregate. Can be empty, in which case all grouping and subgrouping are aggregated. Controlling the rounding on a subset of margins will improve the run-time but will leave the other margins free to potentially deviate far from their original values.
- **var**               : column to be rounded
- **distance_max**      : whether or not to include the maximum distance in the list of distances used to sort partial solutions. Not including it reduces the run-time. Default is False.
- **distance_total**    : whether or not to add the distance on the margin with the distance on the interior cells as a sorting criterion. If True sorting will be done according to this sum instead of the margin sum then interior sum. Default is False.
- **rounding_base**     : the rounding base. Has to be greater than 0. Default is 1.
- **fix_rounding_dist** : if an entry is close to a rounded value by p% of the rounding base, round that entry to its closest rounded value and remove the other rounded value from consideration for that entry. This reduces the search space and execution time at the cost of the quality of the solution. Default is 0 which means that cells that are already exactly rounded won't change.
- **max_heap_size**     : the maximum size of the heap. Has to be greater than 2. Default is 100. A smaller heap will lead to faster execution at the cost of the quality of the solution.

**output:**  
A dictionary with the following keys:
- **input_table**     : the original input data with columns listed in the "by" and "var" input parameters.
- **input_margins**   : the margins of the input table
- **rounded_table**   : the rounded solution of input data with columns listed in the "by" and "var" input parameters.
- **rounded_margins** : the margins of the rounded table
- **distances**       : the distances function's value for the solution
- **opt_report**      : a dictionary containing information about the optimisation process with the following keys:
  - **n_iterations**  : the number of partial solutions expanded
  - **n_heap_purges** : the number of times the heap was purged, keeping the best solutions so far
  - **n_sol_purged**  : the total number of partial solutions that got purged and never further expanded
  - **n_cells**       : the number of entries in the input table
  - **n_margins**     : the number of margin values from the input table
  - **n_fixed_cells** : the number of cells where the rounding is fixed and not subject to the optimisation process


**generate_random_table(n_dim,n_cat,scale):**  
Creates a table filled with random values with the desired number of dimensions and number of categories per dimensions.  

**input:**  
- n_dim : number of dimensions
- n_cat : number of categories per dimensions
- scale : the scale of the numbers in the table: 0 < number < scale.

**output:**  
The generated the table as a pandas dataframe. With columns:  
- 0,1,2 ... n_dim-1 : each column contains values from 0 to n_cat-1.     
- value : contains a random value between 0 and scale.  


## Example
'''python
from CtrlRound import ctrl_round  
from CtrlRound import generate_random_table  

# Generate a test table with 3 dimensions and 5 categories per dimension.  
test = generate_random_table(3, 5, scale=2) 
# Here we use the total distance (sum on the margins and interior cells) and we force the rounding of values that are 10% or less away from their bounds.  
rounded = ctrl_round(test, by=[0,1,2], var="value", rounding_base=1, distance_total=True, fix_rounding_dist=0.1)  
print(rounded)  

# Here we control the rounding on some margin but not all. The grand total is included and denoted by the empty list  
rounded = ctrl_round(test, by=[0,1,2], margins= [[0],[1,2],[] ], var="value")  
print(rounded) 
'''

## License  
This project is licensed under the MIT License -
see the [LICENSE](LICENSE) file for details.

## Changelog   
For detailed information on changes between versions, see the [CHANGELOG.md](CHANGELOG.md).



