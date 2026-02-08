from . import CtrlRound  
from . import generate_table 

# Now pull the functions out of them
ctrl_round = CtrlRound.ctrl_round
generate_random_table = generate_table.generate_random_table

__author__ = "Christian Gagné"
__version__ = "0.6.0"
__all__ = ["ctrl_round", "generate_random_table"]
