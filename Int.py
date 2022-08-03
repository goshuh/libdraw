from __future__ import annotations
from   typing   import Any, Iterator, Union

import numpy  as np
import pandas as pd


__all__ = ['Misc']


class Misc(object):
    
    @staticmethod
    def valid(i: Any) -> bool:
        return i is not None

    @staticmethod
    def identity(i: Any, d: Any = None) -> Any:
        return i if i is not None else d

    @staticmethod
    def flatten(*ds: Union[Any, Iterator[Any]]) -> Iterator[Any]:
        for d in ds:
            if isinstance(d, (list, tuple, map, np.ndarray, pd.Index)):
                yield from Misc.flatten(*d)
            else:
                yield d
