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



# WARNING: Don't use print on Windows. Errors like "UnicodeEncodeError: 
# 'charmap' codec can't encode character '\u015f'" can occur

# NOTE(armagan): 512 bytes seem reasonable for the first pass (0th pass is always size pass).
# NOTE(armagan): 8 kilo bytes seem reasonable for the second pass.
# TODO(armagan): For printing paths, split filename, write filename first.
# then write its path.

# TODO(armagan): Create a shared parameter for grouper functions. Pass it to apply_multiple_groupers function. Inside that, use that shared area to communicate between groupers. ?Make the parameter a list of dictionaries?


import time

# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]
from common_types import *
import constants as CONST
from classes import *
import util as UT
import grouper_funs as GRPR




#from memory_profiler import profile

#@profile
def main_4(out_fpath, IN_PATHS: List[str], SMALLEST_FSIZE):
    # TODO(armagan): Use params Dict of size grouper to both filter and group.
    string_seq: List = []
    
    string_seq.extend( ["======= filedups-main-4 function begining ======= "] )
    string_seq.append('\n')
    
    now_str = UT.get_now_str()
    
    string_seq.extend( ["Start datetime ISO-8601 = {}".format(now_str)] )
    string_seq.append('\n')
    
    string_seq.append("Paths: ")
    string_seq.extend( IN_PATHS )
    string_seq.append('\n')
    
    TM_beg = time.perf_counter()
    
    #print("HASH_BYTES=", HASH_BYTES)

    # string_seq.extend( ["HASH_SIZE(bytes)=", HASH_SIZE] )
    # string_seq.append('\n')
    
    string_seq.extend( ["SMALLEST_FSIZE(bytes)=", SMALLEST_FSIZE] )
    string_seq.append('\n')

    
    fls_unfiltered: Set[str] = UT.get_fpaths_from_path_iter(IN_PATHS)
    
    if len(fls_unfiltered) < 2:
        string_seq.append("Can't find files for given paths. Try giving absolute paths.")
        stringified = map(str, string_seq)
        UT.append_file_text_utf8(out_fpath, ' '.join(stringified))
        return None
    
    SMALLEST_SIZE: int = SMALLEST_FSIZE
    
    def flt_size(path: str):
        #
        try:
            sz: MaybeInt = UT.get_file_size_in_bytes(path)
            if is_nothing(sz):
                return False
            #
            if extract_some(sz) >= SMALLEST_SIZE:
                return True
            #
            return False
        #
        except: # TODO(armagan): Report/except when exception occurs.
            return False
    #
    
    #string_seq.extend( ["Using size filter. Size(bytes)=", SMALLEST_SIZE] )
    #string_seq.append('\n')
    
    #locations: Set[str] = set(filter(flt_size, fls_unfiltered))
    
    # fls: Set[str] = UT.get_nonzero_length_files(IN_PATHS)
    
    string_seq.extend( ["Total number of files to search=", len(fls_unfiltered)] )
    string_seq.append('\n')
    

    fsinfo = FilesInfo(fls_unfiltered, UT.local_file_reader, \
                        UT.get_local_file_size)

    FINDX = FileIndexer([fsinfo])
    
    # TODO(armagan): Use DuplicateFinder class and group function(s).
    FINDER: DuplicateFinder = DuplicateFinder(FINDX, 0.5)
    all_indices: Set[int] = FINDER.get_file_indexer().get_all_indices()
    
    hash_size_1 = 512 * CONST.xBYTE
    hash_size_2 = 64 * CONST.xKB
    hash_size_3 = 1 * CONST.xMB
    
    hs = [hash_size_1, hash_size_2, hash_size_3]
    
    grouper_funcs: List[GroupFunc_t] = [ GRPR.group_by_size \
        , GRPR.sha512_first_X_bytes(X=hs[0]) \
        , GRPR.sha512_first_X_bytes(X=hs[1]) ]
        # , GRPR.sha512_first_X_bytes(X=hs[2]) ]
    
    size_grpr_param = {"minimum_file_size": SMALLEST_FSIZE}
    initial_param = [size_grpr_param, dict(), dict()]
    
    
    string_seq.extend( [ "Groupers=size,{}-hash,{}-hash".format(hs[0],hs[1]) ] )
    string_seq.append('\n')
    
    found_groups_and_extras: Tuple[LocationGroups_t, List] = \
        FINDER.apply_multiple_groupers(all_indices, grouper_funcs, \
                                        shared_mem=initial_param)
    
    found_groups: LocationGroups_t = found_groups_and_extras[0]
    extra_datas: List = found_groups_and_extras[1]
    
    # print(extra_datas)
    # return -1
    
    if len(extra_datas) > 1:
        size_data = extra_datas[1]
    else:
        size_data = dict()
    """
    size_group: LocationGroups_t = FINDER.apply_one_grouper(all_indices,\
                                                        GRPR.group_by_size)
    #
    """
    
    i = 0
    for seq in found_groups:
        if len(list(seq)) < 2:
            continue # Skip unique files.
        
        string_seq.append("+++++++++++ [Group {}] start +++++++".format(i))
        string_seq.append('\n')
        
        for loc_idx in seq:
            # TODO(armagan): This is an ugly way and code. Use PyConst or
            # immutable data structures instead of class/objects.
            # ??https://github.com/tobgu/pyrsistent
            
            loc = FINDER.get_file_indexer().get_location(loc_idx)
            
            sz = -1
            if len(size_data) > 1:
                sz = size_data[loc_idx]
            
            
            
            string_seq.extend( [ "---> File path:", loc ])
            string_seq.append('\n')
            string_seq.extend( [ "-> File name:", UT.get_path_basename(loc) ] )
            string_seq.append('\n')
            if sz > 0:
                string_seq.extend( [ "-> File size:", sz, " bytes. ", int(sz/1024), " kilobytes." ])
                string_seq.extend( [ "{:.2f}".format(sz/(1024*1024)), " megabytes."  ])
            string_seq.append('\n')
        #
        string_seq.append("----------- [Group {}] END -------".format(i))
        string_seq.append('\n')
        string_seq.append('\n')
        
        i += 1
    #
    """"""
    TM_end = time.perf_counter()

    #print("ELAPSED:",TM_end - TM_beg)
    
    string_seq.extend( ["End datetime ISO-8601 = {}".format(UT.get_now_str())] )
    string_seq.append('\n')
    
    string_seq.extend( ["ELAPSED:",TM_end - TM_beg, "seconds."] )
    string_seq.append('\n')
    
    indices: List[int] = FINDX.get_all_indices()
    
    #print(len(indices))
    string_seq.extend( ["Processed ", len(indices), " files."] )
    string_seq.append('\n')
    
    string_seq.extend( ["**********************************************************************"] )
    string_seq.append('\n')
    
    
    stringified = map(str, string_seq)
    
    UT.append_file_text_utf8(out_fpath, ' '.join(stringified))
#


def trials(trial_count: int, search_paths: List[str]):
    NOW = UT.get_now_str()

    for i in range(trial_count):
        smallest_file_size: int = 500 * CONST.xKB # 1.44 MB = some floppy disc capacity
        
        OUTFILE_PATH = "{}_at least({} bytes).txt".format(NOW, smallest_file_size)

        #search_paths_WINDOWS = ["D:\ALL BOOKS-PAPERS", "D:\Documents", "D:\HxD", "D:\Program Files"]

        """
        _search_paths_MINT = ["/media/genel/Bare-Data/ALL BOOKS-PAPERS/" \
        , "/media/genel/Bare-Data/Documents/" \
        , "/media/genel/Bare-Data/HxD/" \
        , "/media/genel/Bare-Data/Program Files/"]
        """
        
        """
        _search_paths = ["/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Aile fotolar, videolar/" \
        , "/media/genel/SAMSUNG/NOT SAMS/Aile family/"]
        # search_paths_MINT = "/media/genel/SAMSUNG/NOT SAMS/Alltxt files/"
        """
        
        # _search_paths_MINT = ["/media/genel/Bare-Data/"]
        
        # _search_paths_MINT = ["/home/genel/"]
        
        # _search_paths = ["/home/genel/"]
        
        # _search_paths = ["/media/genel/Bare-Data/"]
        
        # TODO(armagan): Combine 1 byte size filter and size grouper for performance.
        
        main_4(OUTFILE_PATH, search_paths, smallest_file_size)
    #

    """
    350871 items, totalling 759,9 GiB (815.983.211.147 bytes) = ext-disk,NOT SAM
    """

#


def group_local_files(IN_PATHS: List[str], \
        GROUP_FUNCS: List[GroupFunc_t]) -> Tuple[LocationGroups_t,List]:
    # TODO(armagan): ??? Make this a separate class.
    
    paths_unfiltered: Set[str] = UT.get_fpaths_from_path_iter(IN_PATHS)
    
    fsinfo = FilesInfo(paths_unfiltered, UT.local_file_reader, \
                        UT.get_local_file_size)
    #
    FINDX = FileIndexer([fsinfo])
    
    FINDER: DuplicateFinder = DuplicateFinder(FINDX, 0.5)
    
    all_indices: Set[int] = FINDER.get_file_indexer().get_all_indices()
    
    result: Tuple[LocationGroups_t,List] = FINDER.apply_multiple_groupers( \
                                    all_indices, GROUP_FUNCS, [])
    #
    found_groups = result[0]
    extra_datas: List = result[1]
    
    return result
#


def local_grouper_main(IN_PATHS: List[str]):
    # TODO(armagan): Make this a separate class.
    SMALLEST_FSIZE: int = 1 * CONST.xBYTE
    hs1 = 512
    hs2 = 4 * CONST.xKB
    
    grouper_funcs: List[GroupFunc_t] = [ GRPR.group_by_size \
        , GRPR.sha512_first_X_bytes(X=hs1) \
        , GRPR.sha512_first_X_bytes(X=hs2) ]
    #
    string_seq: List = []
    
    string_seq.extend( ["======= filedups local_grouper_main beginning ======= "] )
    string_seq.append('\n')
    
    now_str = UT.get_now_str()
    
    string_seq.extend( ["Start datetime ISO-8601 = {}".format(now_str)] )
    string_seq.append('\n')
    
    string_seq.append("Paths: ")
    string_seq.extend( IN_PATHS )
    string_seq.append('\n')
    
    string_seq.extend( ["SMALLEST_FSIZE(bytes)=", SMALLEST_FSIZE] )
    string_seq.append('\n')
    
    TM_beg = time.perf_counter()
    
    # TODO(armagan): Continue writing this function.
    
#


if __name__ == "__main__":
    # 
    search_paths_MINT = ["/media/genel/Bare-Data/ALL BOOKS-PAPERS/" \
        , "/media/genel/Bare-Data/Documents/" \
        , "/media/genel/Bare-Data/HxD/" \
        , "/media/genel/Bare-Data/Program Files/"]
    #
    
    search_paths_WIN10 = [r"D:\ALL BOOKS-PAPERS" \
        , r"D:\Documents" \
        , r"D:\HxD" \
        , r"D:\Program Files"]
    #
    
    search_paths = [r"D:\ALL BOOKS-PAPERS"] # or "D:/"
    search_paths = ["D:\\"]
    # search_paths = ["C:\Program Files"]
    search_paths = ["C:\\"]
    
    # trials(3, search_paths) # for performance measurement of cold/hot data.
    trial_cnt = 1
    
    trials(trial_cnt, search_paths) # 1 == Just to find local duplicates. More than 1 == repeats the search.
#

