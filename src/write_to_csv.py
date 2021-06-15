#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LICENSE for this project can be found in the file named LICENSE.
Alternatively, it can be found at the end of this document.
"""

import os
import time
import csv

import _util as UT
import _core as CR


def write_duplicates_with_sizes(in_csv_path, out_csv_path):
    
    path = in_csv_path
    
    rows = UT.read_all_csv(path, row_filters=[UT.filter_out_non_path_row, UT.accept_only_if_group])
    file_rows = []

    for row in rows:
        path = row[-1].strip()  # Last element is file path.
        
        p = os.path.abspath(path)
        if os.path.isfile(p):  # TODO(armaganslmn): Log if not file.
            fsize = UT.get_file_size_in_bytes(p)        
            row.insert(1, fsize/1024)  # /1024 for kilobyte
            file_rows.append(row)
        #
        
        #print(s.encode("utf-8"))
        #print(path.encode("utf-8"))
    #
    file_rows.sort(key = lambda row: row[1])
    for row in file_rows:
        # row[1] is a float. Format it to 2 decimal place str.
        fval = row[1]
        row[1] = "{:.2f}".format(fval)
    #
    file_rows.insert(0, ["INFO", "Size is in kilobytes."])
    
    UT.write_to_csv(out_csv_path, file_rows)
#


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
            writer.writerow([UT.PATH_DESCRIPTOR_STR, "{}-{}".format(UT.UNIQUE_ROW_PREFIX, cnt) + " ", elm])
            
            cnt += 1
        #

        writer.writerow(["-------------Groups below-------------"])

        pcnt = 1
        for k, file_set in fpath_sets.items():
            for fpath in file_set:
                #s = "Group-{}, path: {}".format(pcnt, fpath)
                writer.writerow([UT.PATH_DESCRIPTOR_STR, "{}-{}".format(UT.GROUP_ROW_PREFIX, pcnt) + " ", fpath])
                #print(s.encode("utf-8"))
            #
            #print("-------")
            writer.writerow(["-------"])
            
            pcnt += 1
        #
    # No return. void method
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
