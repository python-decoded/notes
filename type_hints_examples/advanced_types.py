from typing import (Union, Optional, List, Dict, Tuple, TypeAlias, TypeVar, Generic)

String: TypeAlias = str  # будь-який рядок тексту
MyList: TypeAlias = List[int]  # наприклад [1, 2, 3]
MyTuple: TypeAlias = Tuple[str, int, bool]  # наприклад ("foo", 4, True)
MyDict: TypeAlias = Dict[str, int]  # наприклад {"a": 1, "b": 2}
NotRequiredString: TypeAlias = Optional[str]  # будь-який рядок тексту або None
SomeIterable: TypeAlias = Union[list, tuple]  # будь-який ліст або тупл

# Python 3.9+ PEP 585 - Type Hinting Generics In Standard Collections
MyList: TypeAlias = list[int]  # наприклад [1, 2, 3]
MyTuple: TypeAlias = tuple[str, int, bool]  # наприклад ("foo", 4, True)
MyDict: TypeAlias = dict[str, int]  # наприклад {"a": 1, "b": 2}

# Python 3.10+ PEP 604 - Allow writing union types as X | Y

NotRequiredString: TypeAlias = str | None  # будь-який рядок тексту або None
SomeIterable: TypeAlias = list | tuple  # будь-який ліст або тупл


# python 3.12+  ключове слово type

type String = str  # будь-який рядок тексту
type MyList = List[int]  # наприклад [1, 2, 3]
type MyTuple = Tuple[str, int, bool]  # наприклад ("foo", 4, True)
type MyDict = Dict[str, int]  # наприклад {"a": 1, "b": 2}
type NotRequiredString = Optional[str]  # будь-який рядок тексту або None
type SomeIterable = Union[list, tuple]  # будь-який ліст або тупл

# Python 3.9+ PEP 585 - Type Hinting Generics In Standard Collections

type MyList = list[int]  # наприклад [1, 2, 3]
type MyTuple = tuple[str, int, bool]  # наприклад ("foo", 4, True)
type MyDict = dict[str, int]  # наприклад {"a": 1, "b": 2}

# Python 3.10+ PEP 604 - Allow writing union types as X | Y

type NotRequiredString = str | None  # будь-який рядок тексту або None
type SomeIterable = list | tuple  # будь-який ліст або тупл
