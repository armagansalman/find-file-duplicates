#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LICENSE for this project can be found in the file named LICENSE.
Alternatively, it can be found at the end of this document.
"""

# import...
import itertools

import util as UT


def should_accept_file(fpath, filter_funcs):
    # TODO(armaganslmn): Use related func. from util.
    return UT.should_accept_element(fpath, filter_funcs)
#


def filter_files(fpath_iter, filter_funcs):
    passed_fpaths = []
    
    for fpath in fpath_iter:
        try:
            if should_accept_file(fpath, filter_funcs):
                passed_fpaths.append(fpath)
            #
        #
        except Exception as ex:  # TODO(armganslmn): Proper logging, error handling
            #s = "Error on path: {}".format(fpath)
            #s.encode("utf-8")
            #print(s)
            print(UT.get_exception_message(ex))
    #
    return passed_fpaths
#


def group_potentially_same_files(file_paths_iter, key_function):
    all_groups = dict()
    for path in file_paths_iter:
        try:
            key = key_function(path)
            if key in all_groups:
                st = all_groups[key]  # Get group set.
                st.add(path)
            #
            else:
                st = set()
                st.add(path)
                all_groups[key] = st
            #
        #
        except Exception as ex:  # TODO(armganslmn): Proper logging, error handling
            #s = "Error on path: {}".format(path)
            #s.encode("utf-8")
            #print(s)
            print(UT.get_exception_message(ex))
        #
    #
    return all_groups
#


def separate_uniques(groups_dict):
    uniques = set()
    duplicate_groups = dict()
    
    UNIQUE_FILE_SET_SIZE = 1
    for ky,file_set in groups_dict.items():
        if len(file_set) == UNIQUE_FILE_SET_SIZE:
            uniques.add(file_set.pop())
            continue
        #
        else:  # Potentially same files in the set.
            duplicate_groups[ky] = file_set
        #
    #
    return {"uniques":uniques, "potential_duplicates":duplicate_groups}
#


def fpath_iterable_from_group_sets(group):
    """ key, group[key] == key, set of paths """
    return itertools.chain.from_iterable(group.values())
#


def separate_uniques_and_duplicates(fpath_iter, group_fun_sequence):
    fpaths = fpath_iter
    groups = dict()
    uniques = set()
    
    for group_fun in group_fun_sequence:
        groups = group_potentially_same_files(fpaths, group_fun)
        dct = separate_uniques(groups_dict=groups)  # Seperate uniques from potentially same file groups.
        
        groups = dct["potential_duplicates"]
        uniques.update(dct["uniques"])
        
        fpaths = fpath_iterable_from_group_sets(groups)  # Get file paths only as an iterator.
    #
    return [uniques, groups]  # TODO(armaganslmn): Decide whether to return groups or groups.values()?
#


"""
def group_fpaths_sequentially(fpath_iter, group_fun_sequence):
    fpaths = fpath_iter
    groups = dict()
    
    for group_fun in group_fun_sequence:
        groups = group_potentially_same_files(fpaths, group_fun)
        fpaths = fpath_iterable_from_group_sets(groups)
    #
    return groups  # TODO(armaganslmn): Decide whether to return groups or groups.values()?
#
"""

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
