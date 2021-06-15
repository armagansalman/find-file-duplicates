"""
TODO(armaganslmn): Log errors to a file. Don't print them.
TODO(armaganslmn): How much time does it take to list all files in root path: "/"

NOTDO(armaganslmn): Add is_recursive and should_ignore options for PATHs. NO!
NOTDO(armaganslmn): Add ignore path capability.

1) Get paths
2) Find and separate uniques and duplicates.
3) write them down to .csv (named datetime)
4) Read that .csv and get sizes for duplicate PATH's.
5) Sort by size.
6) Write results to another .csv.
"""

import time
import csv

import _util as util
import _core as core
import _write_to_csv as WR

"""
folder_paths = [ r"/home/armagan/Desktop/" ]
#folder_paths = [ r"/home/armagan/Desktop/wxHexEditor-master/COMPILE" ]

folder_paths = [r'/']

start_datetime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

fpaths = util.get_fpaths_from_all_paths(paths_iter = folder_paths)

filtered_fpaths = core.filter_files(fpath_iter=fpaths, \
                                filter_funcs=[util.accept_at_least_X_kb])

hash_func = util.file_sha512_generator(size_to_read=4*1024)

csv_name = "_out_duplicates_"+str(start_datetime)+".csv"

#write_results(csv_name, accepted_fpaths, fpaths, group_func_sequence)
WR.write_results(csv_name, filtered_fpaths, fpaths, [util.get_file_size_in_bytes, hash_func])

group_out_csv = "group"+csv_name
WR.write_duplicates_with_sizes(csv_name, group_out_csv)

"""
###################################################################
# Now, using found potential duplicate files (group .csv file),
# check for duplicates with a bigger hash size.

group_out_csv = "group_out_duplicates_2021-04-21-16-25-47.csv"

run_idx = 2

folder_paths = util.read_paths_from_csv(group_out_csv)

start_datetime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

fpaths = util.get_fpaths_from_all_paths(paths_iter = folder_paths)

# TODO(armaganslmn): Filtering is unnecessary if files are taken from previous run.
# Use them as-is.

filtered_fpaths = core.filter_files(fpath_iter=fpaths, \
                                filter_funcs=[util.accept_at_least_X_kb])

hash_func = util.file_sha512_generator(size_to_read=64*1024)

csv_name = str(run_idx)+"_out_duplicates_"+str(start_datetime)+".csv"

#write_results(csv_name, accepted_fpaths, fpaths, group_func_sequence)
WR.write_results(csv_name, filtered_fpaths, fpaths, [util.get_file_size_in_bytes, hash_func])

group_out_csv = "group"+csv_name
WR.write_duplicates_with_sizes(csv_name, group_out_csv)
