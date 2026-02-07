from CtrlRound import ctrl_round  
from CtrlRound import generate_random_table  

test = generate_random_table(3, 5, scale=2) 
# Here we use the total distance (sum on the margins and interior cells) and we force the rounding of values that are 10% or less away from their bounds.  
rounded = ctrl_round(test, by=[0,1,2], var="value", rounding_base=1, distance_total=True, fix_rounding_dist=0.1)  
assert rounded not None
