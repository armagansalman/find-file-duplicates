#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LICENSE for this project can be found in the file named LICENSE.
Alternatively, it can be found at the end of this document.
"""


#import find_file_duplicates.util

import util as UT
import core as CR


folder_paths = [ r"D:\IMAGES",
                    r"D:\\" ]

folder_paths = [ r"E:\NOT SAMSUNG"]

##
  
folder_paths = [ r"D:\\" ]

folder_paths = [ r"/home/ulimited/Documents/TO WINDOWS/Software source code/find_duplicate_files_project/src/find_file_duplicates/" ]

fpaths = UT.get_fpaths_from_all_paths(paths_iter = folder_paths)

def accept_at_least_X_kb(fpath, X=1*1024):  # X = minimum file size.
    return UT.get_file_size_in_bytes(fpath) >= X
#


accepted_fpaths = CR.filter_files(fpath_iter=fpaths, \
                                filter_funcs=[accept_at_least_X_kb])

all_groups = CR.group_potentially_same_files(accepted_fpaths, UT.get_file_size_in_bytes)

fpath_sets = CR.group_fpaths_sequentially(accepted_fpaths, group_fun_sequence=[UT.get_file_size_in_bytes, UT.get_file_size_in_bytes])

for k, st in fpath_sets.items():
    print(k, st)
    print("")

exit(0)

for key,val in all_groups.items():
    print(key)
    print(val)
    print("")
#

fpaths = CR.fpath_iterable_from_group_sets(all_groups)
for el in fpaths:
    print(el)
    print("")
#

exit(0)


size_fpath_tuples = list()
#for p in fpaths:
for p in accepted_fpaths:
    sz = UT.get_file_size_in_bytes(p)
    sz /= (1024*1024)  # mb
    size_fpath_tuples.append((sz, p))
#

size_fpath_tuples.sort(key=lambda x: x[0])

for pair in size_fpath_tuples:
    s = "Size:{:.3f}_mb; path: {}".format(pair[0], pair[1])
    print(s.encode("utf-8"))
#




"""
MIT License

Copyright (c) 2021 Armağan Salman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
