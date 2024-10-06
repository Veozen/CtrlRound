import heapq
import distance
import best_first_search


# Example usage
possible_cell_values = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
}
initial_values = {
    'A': 1,
    'B': 4,
    'C': 7
}
constraints = {
    'X': ['A', 'B'],
    'Y': ['B', 'C'],
    'Z': ['A', 'C']
}
constraint_values = {
    'X': 10,
    'Y': 15,
    'Z': 12
}

result = best_first_search(possible_cell_values, initial_values, constraints, constraint_values, NSolutions = 16)
print(result)