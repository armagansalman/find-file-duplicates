#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LICENSE for this project can be found in the file named LICENSE.
Alternatively, it can be found at the end of this document.
"""


#import find_file_duplicates.util

import time
import csv

import _util as UT
import _core as CR

# TODO(armaganslmn): Take 'separate_uniques_and_duplicates' out from write.
def write_results(csv_name, accepted_fpaths, fpaths, group_func_sequence):
    with open(csv_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=UT.CSV_DELIMITER,
                                quotechar=UT.CSV_QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
                                
        writer.writerow( ["Filtered to {} files from {} files.".format(len(accepted_fpaths), len(fpaths))] )
        writer.writerow(["Start time" + " "," " + time.asctime()])

        uniques, fpath_sets = CR.separate_uniques_and_duplicates(accepted_fpaths, group_fun_sequence=group_func_sequence)

        finish_datetime = time.asctime()
        writer.writerow(["Finish time" + " "," " + finish_datetime])   

        # Write unique file paths to csv.
        cnt = 1
        for elm in uniques:
            #s = "Unique-{}, path: {}".format(cnt, elm)
            writer.writerow([UT.PATH_DESCRIPTOR_STR, "Unique-{}".format(cnt) + " ", elm])
            
            cnt += 1
        #

        writer.writerow(["-------------Groups below-------------"])

        pcnt = 1
        for k, file_set in fpath_sets.items():
            for fpath in file_set:
                #s = "Group-{}, path: {}".format(pcnt, fpath)
                writer.writerow([UT.PATH_DESCRIPTOR_STR, "Group-{}".format(pcnt) + " ", fpath])
                #print(s.encode("utf-8"))
            #
            #print("-------")
            writer.writerow(["-------"])
            
            pcnt += 1
        #
#

"""

#folder_paths = [ r"/home" ]

folder_paths = [ r"/home/armagan/Desktop/" ]

folder_paths = [ r"/home" ]

folder_paths = [ r"/" ]

start_datetime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

fpaths = UT.get_fpaths_from_all_paths(paths_iter = folder_paths)

tmp_datetime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

#TODO(Log, instead of print.)
#print(start_datetime)
#print("Walked over all files. " + tmp_datetime)

#exit(0)

def accept_at_least_X_kb(fpath, X=100*1024):  # X = minimum file size in bytes.
    return UT.get_file_size_in_bytes(fpath) >= X
#

filtered_fpaths = CR.filter_files(fpath_iter=fpaths, \
                                filter_funcs=[accept_at_least_X_kb])

# all_groups = CR.group_potentially_same_files(accepted_fpaths, UT.get_file_size_in_bytes)

hash_func = UT.file_sha512_generator(size_to_read=4*1024)

# TODO(armaganslmn): Write results to .csv

#time.time()



csv_name = "_out_duplicates_"+str(start_datetime)+".csv"
#write_results(csv_name, accepted_fpaths, fpaths, group_func_sequence)
write_results(csv_name, filtered_fpaths, fpaths, [hash_func])
"""

#exit(0)
#######################################

"""
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
