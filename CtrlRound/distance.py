"""
Utility module to provide disntance functions for controlled rounding

all distance functions must access input parameters partial_solution, initial_values, constraints, constraint_values
"""


def define_interior_distance(func, normalized=True):
    """
    Creates a function to calculate distance from the interior cells
    """
    def calculate_distance(n_cell, initial_values, new_values, initial_constraint_values, new_constraint_values):
        discrepancies = [0]
        n_cell= max(n_cell,1)
        discrepancies = [abs(initial_values[id] - new_values[id]) for id in new_values]
        result = func(discrepancies)
        if normalized:
            result = result/n_cell
        return result
    return calculate_distance

def define_margin_distance(func, normalized=True):
    """
    Creates a function to calculate distance from the margins
    """
    def calculate_distance(n_cell, initial_values, new_values, initial_constraint_values, new_constraint_values):
        discrepancies = [0]
        n_cell= max(n_cell,1)
        discrepancies = [abs(initial_constraint_values[id] - new_constraint_values[id]) for id in new_constraint_values]
        result = func(discrepancies)
        if normalized:
            result = result/n_cell
        return result
    return calculate_distance

def define_total_distance(normalized=True):
    """
    Creates a function to calculate distance from the margins and interior cells
    """
    calculate_margin_distance   = define_margin_distance(sum, normalized=normalized)
    calculate_interior_distance = define_interior_distance(sum, normalized=normalized)

    def calculate_total_distance(n_cell, initial_values, new_values, initial_constraint_values, new_constraint_values):
        return calculate_margin_distance(n_cell, initial_values, new_values, initial_constraint_values, new_constraint_values) + calculate_interior_distance(n_cell, initial_values, new_values, initial_constraint_values, new_constraint_values)

    return calculate_total_distance

# the _accumulate functions, take the discrepancy accumulated on the inner cells so far as a parameter. improves execution time for the _interior_distance and _total_distance functions
def define_accumulate_interior_distance(func, normalized=True):
    """
    Creates a function to accumulate distance from the interior cells
    """
    def calculate_distance(n_cell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values):
        if n_cell > 0 :
            new_discrepancy = abs(initial_values[cell_id] - new_values[cell_id])
            inner_discrepancy = func([inner_discrepancy*(n_cell-1), new_discrepancy] )
        n_cell= max(n_cell,1)
        if normalized:
            inner_discrepancy = inner_discrepancy/n_cell
        return inner_discrepancy
    return calculate_distance

def define_accumulate_margin_distance(func, normalized=True):
    """
    Creates a function to accumulate distance from the margins
    """
    def calculate_distance(n_cell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values):
        discrepancies = [0]
        n_cell= max(n_cell,1)
        discrepancies = [abs(initial_constraint_values[id] - new_constraint_values[id]) for id in new_constraint_values]
        result = func(discrepancies)
        if normalized:
            result = result/n_cell
        return result
    return calculate_distance

def define_accumulate_total_distance(normalized=True):
    """
    Creates a function to accumulate distance from the margins and interior cells
    """
    calculate_margin_distance    = define_accumulate_margin_distance(sum, normalized=normalized)
    accumulate_interior_distance = define_accumulate_interior_distance(sum, normalized=normalized)

    def calculate_total_distance(n_cell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values):
        margin_distance = calculate_margin_distance(n_cell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values)
        inner_distance  = accumulate_interior_distance(n_cell, cell_id, inner_discrepancy, initial_values, new_values, initial_constraint_values, new_constraint_values)
        total_distance  = margin_distance + inner_distance
        return [total_distance, margin_distance, inner_distance]

    return calculate_total_distance


