## Description  
Controlled rounding is a technique used in data publishing to ensure that data released for public use meets specific confidentiality requirements. 
The process adjusts the data values by rounding them to a predetermined base in a such a way that the margins of the resulting table remain closer to their original values than they would should the table's entries have been simply rounded to their nearest base.  

Here the solution to this problem is found by applying a best-first-search method where the decision is to round up or down each non-margin entry. Three distance functions are used to sort partial solutions. 
- The max absolute difference between a margin's value and it's original value.  
- The average absolute difference between a margin's value and it's original value. The average is taken over the rounded cells so far.  
- The average absolute difference between a table cell's rounded value and it's original value. The average is taken over the rounded cells so far.  

Ties on the first function are resolved by looking at the second and then third one. The first complete solution found is returned.  

## Usage 

**ctrl_round(df_in, by, var, margins, rounding_base, fix_rounding_dist, max_heap_size):**  
Aggregates a dataframe and perform controlled rounding of it's entries.  

**input:**  
- **df_in**             : pandas DataFrame
- **by**                : list of column names on which to aggregate the input DataFrame
- **margins**           : list of lists of column names indicating which grouping to aggregate. Can be empty, in which case all grouping and subgrouping are aggregated. Controlling the rounding on a subset of margins will improve the run-time but will leave the other margins free to potentially deviate far from their original values.
- **var**               : column to be aggregated
- **rounding_base**     : the rounding base. Has to be greater than 0.
- **fix_rounding_dist** : if an entry is close to a rounded value by p% of the rounding base, round that entry to its closest rounded value and remove the other rounded value from consideration for that entry. This reduces the search space and run time at the cost of the quality of the solution.
- **max_heap_size**     : the maximum size of the heap. Has to be greater than 2. Default is 1000. A smaller heap will lead to faster run-time at the cost of the quality of the solution.

**output:**  
A dictionary with the following keys:
- **input_table**     : the original input data with columns listed in the "by" and "var" input parameters.
- **input_margins**   :
- **rounded_table**   : the rounded solution of input data with columns listed in the "by" and "var" input parameters.
- **rounded_margins** :
- **objectives**      : the objective function's value for the solution
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

test = generate_random_table(3, 5, scale=2)  
ctrl_round(test, by=[0,1,2], var="value", rounding_base=1, fix_rounding_dist=0.1, max_heap_size=100)  

## License
This project is licensed under the MIT License -
see the [LICENSE](LICENSE) file for details.
