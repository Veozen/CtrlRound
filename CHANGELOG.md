# Changelog 

## [0.5.0] - 2025-01-03 

Changed - improved execution time. Distance functions on the margins now use list comprehensions.

## [0.4.0] - 2024-12-01 
Added - maximum discrepancy on the interior cells in now also reported in the output

Added - **__version__** 

Added - **__author__** 

Changed - **objectives** output key is now **distances**

Changed - improved execution time

## [0.3.0] - 2024-11-15 
Fixed - issue that occured when using **distance_total=True**

Fixed - issue when using **margins** with a column not listed in **by**

Changed - default **max_heap_size** is now 100

Changed - improved execution time

## [0.2.0] - 2024-11-02 
Added - **distance_max** input parameter. Controls whether or not to include the maximum distance in the list of distances used to sort partial solutions. Not including it results in fewer partial solutions expanded and reduces the run-time.

Added - **distance_total** input parameter. Controls whether or not to add the distance on the margin with the distance on the interior cells as a sorting criterion. If True sorting will be done according to this sum instead of the margin sum then interior sum.

Added - Progress bar. Displays the progression towards having a complete solution.

Changed - The default distances measures now do not include the maximum margin discrepancy.

Changed - **ctrl_round** will now raise an error when fed invalid input parameters.
 
## [0.1.0] - 2024-10-24 

Added - Initial release with core functionality.
