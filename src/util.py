import os


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
    file_paths = set()
    # TODO(armaganslmn): Handle if input is file.
    # TODO(armaganslmn): ??? Error handling.
    for path in paths_iter:
        file_paths.update( get_fpaths_recursively_from_folder(path) )
    #
    return file_paths
#

