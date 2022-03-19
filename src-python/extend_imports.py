import os
import sys
import copy

#from typing import Iterable as Iter
from typing import List


def extend_import_paths(directory_paths: List[str]):
    # Input can be relative. "../tests" etc. Adds given paths to import search variable. Returns original paths.
    
    assert(type(directory_paths) == list) # must be list of str
    
    isdir = os.path.isdir
    abspath = os.path.abspath
    
    abs_paths = map(lambda x: abspath(x), directory_paths)
        
    # Find new paths using sets:
    orig_paths = copy.deepcopy(sys.path)
    
    sys_paths: Set[str] = set(sys.path)
    abs_set: Set[str] = set(abs_paths)
    
    news = abs_set.difference(sys_paths)
    
    for p in news:
        if isdir(p):
            sys.path.append(p)
        #
    #
    #sys.path.extend(list(news))  # Update import search locations.
    
    #print("New paths: ", '\n'.join(list(news)))
    #print("<<<<<<< END New paths")
    return orig_paths
#

#sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#sys.path.append(r"D:\Documents\temp\ExamplePythonProject\source\Project")

"""
paths_to_add = ["..", "../Project", "../Project", "..\Project\SubDir1\SubDir2" \
            , "..\Project\SubDir1", "19"
]

extend_import_paths( paths_to_add )
"""