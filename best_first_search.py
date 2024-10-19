import heapq

def best_first_search(possible_cell_values, initial_values, constraints, constraint_values, distanceFuncs, NSolutions=0, max_heap_size=1000, reset_heap_fraction=0.75):
    """
    Performs best first search
    input:
      possible_cell_values  : dictionary of all decision variables along of all possible values for each
      initial_values        : dictionary of initial values for each decision variable
      constraints           : dictionary of each contraints to a list of decison variables that aggregate to that constraint's value
      constraint_values     : dictionary of each contraints to the value they shopudl aggregate to
      NSolutions            : the number of solutions to output. The first solutions found.
      distanceFuncs         : list of functions that will be used to calculation a lsit of distances to associate with a current (partial) solution
      max_heap_size         : the maximum size the heap can be. If reached, half the best solutions will be kept.
      reset_heap_fraction   : When the heap reaches it's maximum size, it is trimmed to keep only the most promising solution. This parameter determines the size of the heap after being trimmed as a fraction of the maximum size. 
      This parameter has to be between 0 and 1. The higher the value, the more often heap timming occurs. Each trim inceases run-time.
    """
    # a unique counter for each partial solution pushed in the heap
    counter         = 0
    
    # number of distance functions passed
    nfuncs = len(distanceFuncs)
    
    # the size of the heap after trimming
    reset_heap_size = int(reset_heap_fraction * max_heap_size)
    
    # Priority queue for Best First Search
    pq              = []
    
    #the first solution  is the one where no decision has been made yet
    initial_partial_solution  = {}
    paramList         = [initial_partial_solution,initial_values,constraints,constraint_values]
    initial_distances = [f(*paramList) for f in distanceFuncs]
    initial_state     = (*initial_distances, counter, initial_partial_solution)
    
    heapq.heappush(pq, initial_state)
    
    Solutions = []
    while pq:
        current_total_distance, current_margin_distance, current_interior_distance, current_counter, current_partial_solution  = heapq.heappop(pq)
        
        if len(current_partial_solution) == len(initial_values):
          Solutions.append((current_total_distance,current_margin_distance,current_interior_distance,current_partial_solution))
          
        # output the N first Solutions found
        if NSolutions > 0 and len(Solutions) == NSolutions:
          return Solutions
          
        # Generate neighbors
        for cell_id in possible_cell_values:
            if cell_id not in current_partial_solution:
              for value in possible_cell_values[cell_id]:
                  new_partial_solution          = current_partial_solution.copy()
                  new_partial_solution[cell_id] = value
                  
                  new_paramList                 = [new_partial_solution,initial_values,constraints,constraint_values]
                  new_distances                 = [f(*paramList) for f in distanceFuncs]
                  
                  # a unique counter is stored in the state so that the heap will never attempt at comparing partial soutions distionaries as this would result in an error
                  # if both distances are the same as another element in the heap, at least the counter will be different and used to order the elements
                  counter                       += 1
                  new_state                     = (*new_distances, counter, new_partial_solution)
                  heapq.heappush(pq,new_state)
              break
        
        #if heap gets too large, cut it in half keeping only the best partial solutions
        if len(pq) > max_heap_size:
          pq.sort(key=lambda x: x[:nfuncs])
          pq = pq[:reset_heap_size]
          heapq.heapify(pq)
        
    return Solutions
