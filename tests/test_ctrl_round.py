"""
Tests for CtrlRound package
"""

import pytest
from CtrlRound import ctrl_round, generate_random_table

def test_ctrl_round_basic_execution():
    """
    Tests that ctrl_round produces a result for a random 3x5 table.
    """
    # 1. Setup
    test_table = generate_random_table(3, 5, scale=2)

    # 2. Execution
    # Here we use the total distance (sum on the margins and interior cells) and we force the rounding of values that are 10% or less away from their bounds.  
    rounded = ctrl_round(
        test_table,
        by=[0, 1, 2],
        var="value",
        rounding_base=1,
        distance_total=True,
        fix_rounding_dist=0.1
    )

    # 3. Assertions
    assert isinstance(rounded, dict), f"Expected dict, got {type(rounded)}"
    assert len(rounded) > 0, "The returned dictionary is empty"
