"""
    <This file is a part of the program armaganymmt-prj-1_name.
    armaganymmt-prj-1_name processes files from different kinds of
    locations to find duplicate files.>
    
    Copyright (C) <2021-2022>  <Armağan Salman> <gmail,protonmail: armagansalman>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import util as UT
from common_types import *
from classes import *


def group_by_size(FIDX: FileIndexer, LOCS: LocationIndices_t, \
                    params: Any) -> GrouperReturn_t:
    # TODO(armagan): Combine size filter and group in one grouper for speed.
    
    size_groups: Dict[int, Set[int]] = dict()
    id_to_size = dict()
    
    for IDX in LOCS:
        #LOC = FIDX.get_location(IDX)
        #SFUN = FIDX.get_size_func(IDX)
        LOC, READFUN, SIZEFUN = FIDX.get_file_info(IDX)
        SIZE: Maybe = SIZEFUN(LOC)
        
        # TODO(armagan): Report/except when SIZE == None.
        if is_nothing(SIZE):
            continue
        #
        
        sz: int = extract_some(SIZE)
        
        if sz < params["minimum_file_size"]:
            continue # Skip small files.
        #
        
        # Group location indices which have the same size. Create group if not exists:
        group: Set[int] = size_groups.get(sz, set())
        group.add(IDX)
        size_groups[sz] = group
        
        id_to_size[IDX] = sz
    #
    
    res: List[Set[int]] = list()
    for key, val in size_groups.items():
        res.append(val)
    #
    
    return (res, {"id_to_size_map": id_to_size})
#


def sha512_first_X_bytes(X: int) -> GroupFunc_t:
    #
    def grouper(FIDX: FileIndexer, LOCS: LocationIndices_t, \
                    params: Any) -> GrouperReturn_t:
        #
        hash_groups: Dict[int, Set[int]] = dict()
        
        for IDX in LOCS:
            LOC = FIDX.get_location(IDX)
            read_func = FIDX.get_reader(IDX)
            FIRST_X_BYTES = read_func(LOC, 0, X-1) # end byte idx = X-1
            
            # TODO(armagan): Report/except when FIRST_X_BYTES == None.
            if is_nothing(FIRST_X_BYTES):
                continue
            #
            data: bytes = extract_some(FIRST_X_BYTES)
            
            hex_hash = UT.sha512_bytes(data)
            
            group: Set[int] = hash_groups.get(hex_hash, set())
            group.add(IDX)
            hash_groups[hex_hash] = group
        #
        
        res: List[Set[int]] = list()
        for key, val in hash_groups.items():
            res.append(val)
        #
        accumulated_dict: Dict[Any,Any] = dict()
        
        return (res, accumulated_dict)
    #
    
    return grouper
#

# Type Definitions:                        
#LowMaybe = Optional[int]
#HighMaybe = Optional[int]


def make_filter_group_by_size(low: MaybeInt, high: MaybeInt) \
        -> GroupFunc_t:
    # Creates size grouper functions.
    # TODO(armagan): Complete this function. (2022-03-14)
    def filter_group_by_size(FIDX: FileIndexer, LOCS: LocationIndices_t, \
            params: Any) -> GrouperReturn_t:
        # 4 cases for low,high = 0,0;0,1;1,0;1,1
        return ([{1,2,3}], dict())
    #
    
    return filter_group_by_size
#
