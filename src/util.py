import os
import hashlib


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
