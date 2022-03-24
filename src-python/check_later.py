def group_local_files(IN_PATHS: List[str], \
        GROUP_FUNCS: List[GroupFunc_t]) -> Tuple[LocationGroups_t,List]:
    # TODO(armagan): ??? Make this a separate class.
    
    paths_unfiltered: Set[str] = UTIL.get_fpaths_from_path_iter(IN_PATHS)
    
    fsinfo = FilesInfo(paths_unfiltered, UTIL.local_file_reader, \
                        UTIL.get_local_file_size)
    #
    FINDX = FileIndexer([fsinfo])
    
    FINDER: DuplicateFinder = DuplicateFinder(FINDX)
    
    all_indices: Set[int] = FINDER.get_file_indexer().get_all_indices()
    
    result: Tuple[LocationGroups_t,List] = FINDER.apply_multiple_groupers( \
                                    all_indices, GROUP_FUNCS, [])
    #
    found_groups = result[0]
    extra_datas: List = result[1]
    
    return result
#