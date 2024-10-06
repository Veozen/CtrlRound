import heapq
from distance import calculate_margin_distance, calculate_interior_distance

def best_first_search(possible_cell_values, initial_values, constraints, constraint_values, NSolutions=0, max_heap_size=100):
    counter = 0
    # Priority queue for Best First Search
    pq = []
    initial_partial_solution = {}
    initial_margin_distance          = calculate_margin_distance(initial_partial_solution, initial_values, constraints, constraint_values)
    initial_interior_distance = calculate_interior_distance(initial_partial_solution, initial_values)
    initial_total_distance    = initial_margin_distance + initial_interior_distance
    initial_state = (initial_total_distance, initial_margin_distance, initial_interior_distance, counter, initial_partial_solution)
    heapq.heappush(pq, initial_state)
    
    Solutions = []
    while pq:
        current_total_distance, current_margin_distance, current_interior_distance, current_counter, current_partial_solution  = heapq.heappop(pq)
        
        if len(current_partial_solution) == len(initial_values):
          Solutions.append((current_total_distance,current_margin_distance,current_interior_distance,current_partial_solution))
          
        if NSolutions > 0 and len(Solutions) == NSolutions:
          return Solutions
          
        # Generate neighbors
        for cell_id in possible_cell_values:
            if cell_id not in current_partial_solution:
              for value in possible_cell_values[cell_id]:
                  new_partial_solution = current_partial_solution.copy()
                  new_partial_solution[cell_id] = value
                  new_margin_distance           = calculate_margin_distance(new_partial_solution, initial_values, constraints, constraint_values)
                  new_interior_distance = calculate_interior_distance(new_partial_solution, initial_values)
                  new_total_distance            = new_margin_distance + new_interior_distance
                  # a unique counter is stored in the state so that the heap will never attempt at comparing partial soutions distionaries as this would result in an error
                  # if both distances are the same as another element in the heap, at least the counter will be different and used to order the elements
                  counter += 1
                  new_state =  (new_total_distance, new_margin_distance, new_interior_distance, counter, new_partial_solution)
                  heapq.heappush(pq,new_state)
              break
        
        #if heap gets too large keep only the first N best partial solution
        if len(pq) > 1.5* max_heap_size:
          pq.sort(key = lambda x: (x[0],x[1],x[2],x[3]))
          pq= pq[:max_heap_size]
          heapq.heapify(pq)
        
        
    return Solutions