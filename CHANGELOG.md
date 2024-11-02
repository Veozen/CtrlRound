# Changelog 

## [0.1.2] - 2024-11-01 
### Added - **distance_max** input parameter. Controls whether or not to include the maximum distance in the list of distances used to sort partial solutions. Not including it results in fewer partial solutions expanded and reduces the run-time.

### Changed - The default distances measures now do not include the maximum margin discrepancy.

### Changed - **ctrl_round** will now raise an error when fed invalid input parameters.
 
## [0.1.0] - 2024-10-24 

### Added - Initial release with core functionality.