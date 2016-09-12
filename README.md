# conditioning
Find the conditioning number of a smooth variety based on a finite point sample

# changelog
2016-06-28
- Finalized code for curves in Sage

2016-08-18
- Migrated to GitHub
- Switched to class approach
- Began work on code for surfaces, using code for curves

2016-08-19
- First draft of code for surfaces completed, needs testing
- Corrected Sage functions to package-specific Python functions

2016-08-21
- Split up curve checker into two, changed input class
- Removed numpy dependency

2016-08-24
- Changed cnumaff so it returns only "realistic" cond nums (based on pair ratio)

2016-08-26
- Started work on function for n-dimensional projective varieties defined by 1 function

2016-08-27
- Completed first draft for general conditioning number finder (using nested / recursive tree approach) cnumgen

2016-08-29
- Began working on examples with lots of approximate points (cone10.txt)

2016-09-12
- Consolidated curve conditioning number finder into general number finder, moved helper functions to helpers.py
- Deleted curves.py and surfaces.py, all can be done with cnumgen in main file
- Examples need to be adjusted with respect to the new structure