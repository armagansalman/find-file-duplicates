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


from typing import Callable
# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]

from typing import Iterable as Iter_t
from typing import Sequence

from typing import Any
from typing import AnyStr
from typing import Dict
from typing import Set
from typing import List
from typing import Tuple
from typing import Sized

from typing import TypeVar
# from typing import Optional

# from typing import TypeAlias  # "from typing_extensions" in Python 3.9 and earlier


LocationIndices_t = Set[int]
LocationGroups_t = Iter_t[LocationIndices_t]

GrouperReturn_t = Tuple[LocationGroups_t, Dict[Any,Any]]
# Iterable_t = Iter_t


StartIdx = int
EndIdx = int

Location = Any
ReaderFunc = Callable[[Any, StartIdx, EndIdx], Tuple[bool, bytes]]
SizeFunc = Callable[[Any], Tuple[bool, int]]
# Type Definition:
FileInfoTriple = Tuple[Location, ReaderFunc, SizeFunc]



"""
    Maybe type.
    Implemented as a tuple. For a maybe M, if the first element is None, M is nothing and the value it holds is invalid/meaningless. Else, the data is valid and can be extracted.
"""
Maybe = Tuple[Any, Any]
MaybeInt = Tuple[Any, int]

class InvalidValueError(BaseException):
    pass
#

def make_some(data: Any) -> Maybe:
    return (True, data)
#

def make_nothing() -> Maybe:
    return (None, None) # Second field is unimportant
#

def is_nothing(arg: Maybe) -> bool:
    return arg[0]  == None
#

def is_some(arg: Maybe) -> bool:
    return not is_nothing(arg)
#

def extract_some(arg: Maybe) -> Any:
    if is_some(arg):
        return arg[1]
    else:
        raise InvalidValueError("Given argument is nothing. Can't extract data from a nothing.")
#
