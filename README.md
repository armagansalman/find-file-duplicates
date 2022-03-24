# FIND FILE DUPLICATES
**WARNING: THIS PROJECT IS IN PROGRESS. DO NOT DEPEND ON ANY FUNCTION/CLASS/MODULE**
Given a sequence of paths (directory or file), finds and groups duplicate files recursively.
Doesn't provide 100% accuracy (might report a file as duplicate when it's not).
Average processing speed = near 200 files/second for a cold search on a hard disk on Windows 10.

## HOW TO USE
Current (2022-03-24) use is not user friendly. It will be improved.  
Put paths in a list and assign it to **search_paths** variable in **main.py** under function **def current_main(trial_cnt = 1)**  
Then, from the console, 
**python3 main.py**
or
**python main.py**