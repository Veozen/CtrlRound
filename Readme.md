**ctrl_round(df_in, by, var, margins, rounding_base, fix_rounding_dist, max_heap_size):**  
Aggregates a dataframe and perform controlled rounding of it's entries.  

input:  
>  df_in             : pandas dataframe  
>  by                : list of column names on which to aggregate the input dataframe  
>  margins           : list of list of column name indicating which grouping to aggregate. Can be empty in which case all grouping and subgrouping are aggregated. Controlling the rounding on a subset of margins will improve the run-time but will leave the other margins free to potentialy deviate far from their original values.  
>  var               : column to be aggregated  
>  rounding_base     : the rounding base. Has to be greater than 0.  
>  fix_rounding_dist : if an entry is close to a rounded value by p% of the rounding base, round that entry to it's closest rounded value and remove the other rounded value from consideration for that entry. This reduces the serach space and run time at the cost of the quality of the solution.  
>  max_heap_size     : the maximum size the heap. Has to be greater than 2. Default is 1000. A smaller heap will lead to faster run-time at the cost of the quality of the solution.  
    
output:  
>  A dictionary with following keys:  
>  input_table     : the original input data with columns listed in the "by" and "var" input parameters.   
>  input_margins   :  
>  rounded_table   : the rounded solution of input data with columns listed in the "by" and "var" input parameters.  
>  rounded_margins :  
>  objectives      : the objective functions value for the solution
>  opt_report      : a dictionary containing information about the optimisation process with folowing keys:  
> >   n_iterations   : the number of partial solution expanded  
> >   n_heap_purges  : the number of times the heap was purged, keeping the best solution so far  
> >   n_sol_purged   : the total number of partial solution that got purged and never further expanded  
> < n_cells         : the number of entries in the input table  
> < n_margins       : the number of margin values from the input table   
> < n_fixed_cells   : the number of cells where the rounding is fixed and not subject to the optimisation process  

