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


import pandas as pd
test = pd.DataFrame({
    "x": [1,2,3,1,2,3],
    "y": [10,10,20,20,30,30],
    "id": ["1:10","2:10","3:20","1:20","2:30","3:30"],
    "z": [11,22,33,44,55,66]
})

aggBy(test, "x", "z", "id")

test= generate_random_table(3,5,scale=2)
CtrlRound(test, by=[0,1,2], var="value", roundingBase=1, fixRoundingDist=0.1, maxHeapSize=16000)
