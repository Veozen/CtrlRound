import distance
import best_first_search

test= generate_random_table(3,5,scale=2)
ctrl_round(test, by=[0,1,2], var="value", roundingBase=1, fixRoundingDist=0.1, maxHeapSize=1000)
