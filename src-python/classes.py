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


"""

Design/Decisions/Definitions:
    + A 'file' is an ordered sequence of bytes.
        It has a non-negative size. 
        A slice of its bytes can be read given a 'start_idx' and
        'end_idx'.
    
    + FilesInfo type:
        + Has 'locations' iterable which holds multiple 'location' 
        values. A 'location' can be any type as long as it can be read 
        from a user given reader function.
        
        + Has 'reader_func' function that reads and returns bytes from
        a file. If 'end_idx' is bigger than file length, reads all 
        the way to the end (starting at 'start_idx').
        
            Its signature is:
        byte[] reader_func(location: Any, start_idx: int, end_idx: int)

        + Has 'size_getter' function that returns the number of bytes 
        the file has.
        
            Its signature is:
        non_negative_int size_getter(location: Any)
    
    + FileIndexer type:
        + Why: To easily handle different location types and
        reader functions. For example, a FilesInfo object might hold 
        local files and another one holds links to web documents.
        Core part of the program doesn't have to know about such 
        differences.
        
        + An object of this type (e.g FIDX) assigns every location
        an index (e.g lidx). Using this lidx, its related 'location',
        'reader_func', 'size_getter' can be retrieved in an uniform way
        via FIDX.
        
    + DuplicateFinder type:
        + Accepts a 'FileIndexer' object and a float value that denotes
        how similar can two files be if they are to be grouped as 
        duplicate. For example, 25% means that at least 25% of the files' 
        content starting from index 0 to 25% of the file must be the same.
        
        Concrete example: For 25% similarity constraint,
        file-1 = [0,1,0,0,1,0,1,1]
        file-2 = [1,1,0,0,1,0,1,1]
        these two files would NOT be grouped as duplicates. Because 
        their first element is different.
        
        + Has 'get_file_indexer' function. Returns the FileIndexer member.
        
        + Has 'group_files' function. Takes similarity percentage as float.
        A FileGroup is an iterable of file indices (from FileIndexer).
        'group_files' function returns an iterable of FileGroup elements. 
        
        + TODO(armagan): ???optional byte count constraint.
        + TODO(armagan): ???Make 'DuplicateFinder' just a function interface.
"""


# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]

from common_types import *


def concat_data_with(data_list: list, concatenator: str):
    return concatenator.join(map(str,data_list))


class FilesInfo:
    def __init__(self, locations: Iter_t[Any] \
    , reader_func: ReaderFunc \
    , size_getter: SizeFunc):
    #   
        self.locations: List[Location]  = list(set(locations))
        # set to remove duplicate locations.
        # Ensure it's subscriptable.
        
        self.reader_func = reader_func
        self.size_getter = size_getter
    #
#




class FileIndexer:
    def __init__(self, files_info_iter: Iter_t[FilesInfo]):
        self.data: List[FileInfoTriple] = list()
        # data = [["path1", reader, size_getter], ["path2", ...,...]]
        for files_info in files_info_iter:
            reader: ReaderFunc = files_info.reader_func
            size_fun: SizeFunc = files_info.size_getter
            
            for loc in files_info.locations:
                info: FileInfoTriple = (loc, reader, size_fun)
                    
                self.data.append(info)
            #
        #
    #
    
    
    def get_file_info(self, idx: int) -> FileInfoTriple:
        info: FileInfoTriple = self.data[idx]
        return info
    #
    
    
    def get_location(self, idx: int) -> Location:
        info: FileInfoTriple = self.get_file_info(idx)
        return info[0]
    #
    
    
    def get_reader(self, idx: int) -> ReaderFunc:
        info: FileInfoTriple = self.get_file_info(idx)
        return info[1]
    #
    
    
    def get_size_func(self, idx: int) -> SizeFunc:
        info: FileInfoTriple = self.get_file_info(idx)
        return info[2]
    #
    
    
    def get_max_idx(self) -> int:
        # Total number of locations minus 1.
        return len(self.data)-1
    #
    
    
    def get_all_indices(self) -> List[int]:
        return [x for x in range(self.get_max_idx()+1)]
    #
    
#


# Some type definitions:
MatchPercentage_t = float
GroupFunc_t = Callable[[FileIndexer, LocationIndices_t, \
                        Any], GrouperReturn_t]


class DuplicateFinder:
    def __init__(self, FILE_INDEXER: FileIndexer):
        self.FIDX = FILE_INDEXER
    ##
    
    def get_file_indexer(self):
        return self.FIDX
    ##
    
    def apply_one_grouper(self, LOCS: LocationIndices_t, \
                        GFUNC: GroupFunc_t, iter_num:int) -> GrouperReturn_t:
        #
        given_params = self.shared_mem[iter_num]
        
        res = GFUNC(self.FIDX, LOCS, given_params)
        locs: LocationGroups_t = res[0]
        extra_data: Dict[Any,Any] = res[1]
        
        return (locs, extra_data)
    ##
    
    def rec_apply(self, LOCS: LocationIndices_t, FUNC_IDX: int, \
                    GROUPERS: List[GroupFunc_t]) -> LocationGroups_t:
        #
        locs: Set[int] = set(LOCS)
        
        if len(locs) < 2: # Fewer than 2 files can't be duplicates.
            return [locs]
        #
        
        if FUNC_IDX >= len(GROUPERS): # No grouper function left to apply.
            return [locs]
        #
        
        groups_plus_extras: GrouperReturn_t = self.apply_one_grouper(locs,\
                                                    GROUPERS[FUNC_IDX],\
                                                    FUNC_IDX)
        #
        
        loc_groups = groups_plus_extras[0]
        extras = groups_plus_extras[1]
        
        iter_dict = self.shared_mem[self.iteration]
        
        
        NEXT_FUNC_IDX = FUNC_IDX + 1
        combined_groups: List[LocationIndices_t] = []
        
        for grp in loc_groups:
            sub_grp_result: LocationGroups_t = self.rec_apply(grp, \
                                                NEXT_FUNC_IDX, GROUPERS)
            #
            for sub_grp in sub_grp_result:
                combined_groups.append(sub_grp)
            #
        #
        
        return combined_groups
    ##
    
    def apply_multiple_groupers(self, LOCS: LocationIndices_t, \
                    GROUPERS: List[GroupFunc_t], shared_mem) -> Tuple[LocationGroups_t,List[Any]]:
        # TODO(armagan): ???User MUST ??? match percentage.
        # TODO(armagan): Fix inter-grouper data sharing and make it fast.
        # prms = shared_mem["params"]
        # prms[0] == additional parameters for size grouper (first grouper)
        self.shared_mem = shared_mem
        self.iteration = 0
        # "_".join(["iter",self.iteration])
        #iter_key = concat_data_with(["iter",self.iteration], "_")
        iter_key = "_".join( ["iter", str(self.iteration)] )
        
        self.shared_mem.append({iter_key:dict()})
        
        GROUPER_FUNC_IDX = 0
        
        result_groups: LocationGroups_t = self.rec_apply(LOCS, \
                                            GROUPER_FUNC_IDX, GROUPERS)
        #
        return (result_groups, self.shared_mem)
    ##
    
#

