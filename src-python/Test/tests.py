"""
    ...
"""

import sys

import extend_imports as EI
paths_to_add = ["../"]
orig = EI.extend_import_paths( paths_to_add )

import common_types as CT

nt = CT.make_nothing()

dat = CT.extract_data(nt)

print(">>>", "\n".join(orig))
print()
print(">>>", "\n".join(sys.path))