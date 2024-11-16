import heapq
import sys

def update_progress(progress ):
    barLength : int = 10 # Modify this to change the length of the progress bar
    status    : str = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block : int = int(round(barLength*progress))
    text  : str = "\rProgress ".ljust(10) + " : " + "[{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100,2), status)
    sys.stdout.write(text)
    sys.stdout.flush()


def modify_margins(cell_id, previous_value, new_value, constraints_list, constraint_values ):
  new_constraint_values  = constraint_values.copy()
  for cons in constraints_list:
    new_constraint_values[cons] = new_constraint_values[cons]-previous_value + new_value
  return new_constraint_values


def best_first_search(possible_cell_values, initial_values, constraints, cell_id_constraints, constraint_values, distance_funcs, n_solutions=0, max_heap_size=1000, reset_heap_fraction=0.75):
    """
    Performs best first search
    input:
      possible_cell_values  : dictionary of all decision variables along of all possible values for each
      initial_values        : dictionary of initial values for each decision variable
      constraints           : dictionary of each contraints to a list of decison variables that aggregate to that constraint's value
      cell_id_constraints   : dictionary of each decision variables to a list of constraint to which it adds up.
      constraint_values     : dictionary of each contraints to the value they shopudl aggregate to
      n_solutions           : the number of solutions to output. The first solutions found.
      distance_funcs        : list of functions that will be used to calculation a lsit of distances to associate with a current (partial) solution
      max_heap_size         : the maximum size the heap can be. If reached, half the best solutions will be kept.
      reset_heap_fraction   : When the heap reaches it's maximum size, it is trimmed to keep only the most promising solution. This parameter determines the size of the heap after being trimmed as a fraction of the maximum size. 
      This parameter has to be between 0 and 1. The higher the value, the more often heap timming occurs. Each trim inceases run-time.
    """
    # a unique counter for each partial solution pushed in the heap
    counter           = 0
    n_heap_purges     = 0
    n_sol_purged      = 0
    
    # number of distance functions passed
    nfuncs          = len(distance_funcs)
    # the size of the heap after trimming
    reset_heap_size = int(reset_heap_fraction * max_heap_size)
    
    # list of all decision variables
    cell_id_list    = list(initial_values.keys())
    
    # Priority queue for Best First Search
    pq              = []
    
    #the first solution  is the one where no decision has been made yet
    initial_partial_solution  = {}
    param_list                = [len(initial_partial_solution), initial_values, initial_partial_solution, constraint_values, constraint_values]
    initial_distances         = [f(*param_list) for f in distance_funcs]
    initial_state             = (*initial_distances, counter, initial_partial_solution, constraint_values)
    longest_partial_solution  = 0
    
    heapq.heappush(pq, initial_state)
    
    Solutions = []
    while pq:
        current_best_node         = heapq.heappop(pq)
        current_partial_solution  = current_best_node[-2]
        current_constraint_values = current_best_node[-1]
        current_distances         = current_best_node[:-2]
        
        longest_partial_solution  = max(longest_partial_solution, len(current_partial_solution))
        
        #update progress bar
        update_progress(longest_partial_solution/ len(initial_values)  )
        
        #if the partial solution is complete, store it with objective functions
        if len(current_partial_solution) == len(initial_values):
          Solutions.append((*current_distances, current_partial_solution, current_constraint_values))
          
        # output the N first Solutions found
        if n_solutions > 0 and len(Solutions) == n_solutions:
          return Solutions, counter, n_heap_purges, n_sol_purged
          
        #select a cellID to expland
        cell_id                           = cell_id_list[len(current_partial_solution)]
        current_partial_solution[cell_id] = initial_values[cell_id]
        
        # Generate neighbors
        for value in possible_cell_values[cell_id]:
            new_partial_solution          = current_partial_solution.copy()
            
            new_constraint_values         = modify_margins(cell_id, current_partial_solution[cell_id], value, cell_id_constraints[cell_id], current_constraint_values)
            new_partial_solution[cell_id] = value
            
            new_param_list                = [len(new_partial_solution), initial_values, new_partial_solution, constraint_values, new_constraint_values]
            new_distances                 = [f(*new_param_list) for f in distance_funcs]
            
            # a unique counter is stored in the state so that the heap will never attempt at comparing partial soutions distionaries as this would result in an error
            # if both distances are the same as another element in the heap, at least the counter will be different and used to order the elements
            counter                       += 1
            new_state                     = (*new_distances, counter, new_partial_solution, new_constraint_values)
            heapq.heappush(pq,new_state)
        
        #if heap gets too large, cut it in half keeping only the best partial solutions
        if len(pq) >= max_heap_size:
          pq.sort(key=lambda x: x[:nfuncs])
          n_sol_purged += len(pq) - reset_heap_size
          pq            = pq[:reset_heap_size]
          heapq.heapify(pq)
          n_heap_purges += 1
          
    return Solutions, counter, n_heap_purges, n_sol_purged
