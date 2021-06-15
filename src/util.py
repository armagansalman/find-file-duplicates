#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LICENSE for this project can be found in the file named LICENSE.
Alternatively, it can be found at the end of this document.
"""

import os
import time
import hashlib
import csv


PATH_DESCRIPTOR_STR = "PATH"  # For .csv files. row[0] == PATH implies row[-1] == A_VALID_PATH
CSV_DELIMITER = ';'
CSV_QUOTECHAR = '"'
GROUP_ROW_PREFIX = "Group"
UNIQUE_ROW_PREFIX = "Unique"


def accept_at_least_X_kb(fpath, X=100*1024):  # X = minimum file size in bytes.
    return get_file_size_in_bytes(fpath) >= X
#

def should_accept_element(element, filter_functions):
    for func in filter_functions:
        if func(element) == False:
            return False
        #
    #
    return True
#

def write_to_csv(csv_name, row_list):
    with open(csv_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=CSV_DELIMITER,
                                quotechar=CSV_QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        #
        for row in row_list:
            writer.writerow(row)
        #
    #
#

def read_all_csv(path, row_filters=None):
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=CSV_DELIMITER,
                            quotechar=CSV_QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        #
        line_list = []
        for row in reader:
            if row_filters == [] or row_filters == None:
                line_list.append(row)
            elif should_accept_element(row, row_filters):
                line_list.append(row)
            else:
                continue
            #
        #
        return line_list
    #
#
def accept_only_if_group(row):
    s = row[1]
    s = s.lower()
    s = s.strip()
    return s.startswith(GROUP_ROW_PREFIX.lower())
#

def filter_out_non_path_row(row):
    return row[0] == PATH_DESCRIPTOR_STR
#

def read_paths_from_csv(csv_path):
    # If first element is PATH_DESCRIPTOR_STR, last element of row is a path.
    csv_rows = read_all_csv(csv_path)
    paths = []
    
    for row in csv_rows:
        if should_accept_element(row, [filter_out_non_path_row]):
            path = row[-1]
            path = path.strip()
            paths.append(path)
        #
    #
    return paths
#

"""
TODO(armaganslman): finish chunked read and chunked hash.

def read_in_chunks(fileObj, chunkSize=2048):
    
    #Lazy function to read a file piece by piece.
    #Default chunk size: 2kB.
    
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            break
        #
        yield data
    #
#


def chunked_hash(file_path, buffer_size=4*1024):
    with open(file_path, "rb") as in_fobj:
        for chunk in read_in_chunks(in_fobj):
            
         
    pass
#
"""

def file_sha512_generator(size_to_read):
    def func(file_path):
        return file_sha512(file_path, size_to_read)
    #
    return func
#


def file_sha512(file_path, size_to_read):
    hs = hashlib.sha512()
    data = None
    
    with open(file_path, "rb") as in_fobj:
        data = in_fobj.read(size_to_read)
    #
    
    hs.update(data)
    return hs.hexdigest()
#


def get_fpaths_recursively_from_folder(PATH):
    rec_files = set()
    # TODO(armaganslmn): ??? Error handling.
    if os.path.isfile(PATH):
        rec_files.add(PATH)
        return rec_files
    #
    
    for root, dirs, files in os.walk(PATH):
        for name in files:
            p = os.path.join(root, name)
            rec_files.add(os.path.abspath(p))
        #
    #
    return rec_files
#


def get_fpaths_from_all_paths(paths_iter):
    file_paths = []
    # TODO(armaganslmn): Handle if input is file.
    # TODO(armaganslmn): ??? Error handling.
    for path in paths_iter:
        file_paths.extend( get_fpaths_recursively_from_folder(path) )
    #
    return file_paths
#


def get_file_size_in_bytes(path):
    statinfo = os.stat(path)
    return statinfo.st_size
    """
    try:  # TODO(armaganslmn): Don't use try-except here. Use where it's called.
        statinfo = os.stat(path)
        return statinfo.st_size
        
    except Exception as ex:
        #s = "Error on path: {}".format(path)
        #s.encode("utf-8")
        #print(s)
        print(get_exception_message(ex))
    """
#


def get_exception_message(exception_obj):
    # Just print(e) is cleaner and more likely what you want,
    # but if you insist on printing message specifically whenever possible...
    e = exception_obj
    # TODO(armaganslmn): Don't return encoded. Just return as-is
    if hasattr(e, 'message'):
        return e.message.encode("utf-8")
    else:
        return str(e).encode("utf-8")
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
