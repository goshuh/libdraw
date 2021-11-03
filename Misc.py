from __future__ import annotations
from   typing   import Any, Iterator, Optional, Union

import numpy as np
import pandas as pd

from . import Data


__all__ = ['Wrap']


def valid(i: Optional[Any]) -> bool:
    return i is not None


def identity(i: Optional[Any], d: Any = None) -> Any:
    return i if i is not None else d


def flatten(*ds: Union[Any, Iterator[Any]]) -> Iterator[Any]:
    for d in ds:
        if isinstance(d, (list, tuple, map, pd.Index, np.ndarray)):
            yield from flatten(*d)
        else:
            yield d


class Wrap(object):

    def __init__(self, d: Data.Data, **kw: Any):
        self.__dict__.update(kw)
        self.__dict__['data'] = d

    def __getattr__(self, k: str) -> Optional[Any]:
        if k.startswith('set_'):
            return lambda *a, **kw: self.__setattr__(k.replace('set_', ''), *a, **kw)
        elif k == 'T':
            self.data = self.data.T
            return self
        else:
            return None

    def __setattr__(self, k: str, *a: Any, **kw: Any) -> Wrap:
        if k == 'attr':
            for w, v in kw.items():
                if w not in self.__dict__:
                    self.__dict__[w] = v
        else:
            self.__dict__[k] = a[0] if a else ''

        return self

    def __getitem__(self, k: Any) -> Wrap:
        return Wrap(self.data[k], **self.__dict__)

    def copy(self, w: Wrap) -> Wrap:
        for k, v in w.__dict__.items():
            if k not in self.__dict__:
                self.__dict__[k] = v
        return self

    def save(self, fn: str) -> Wrap:
        self.data.save(fn)
        return self

    def load(self, fn: str, **kw: Any) -> Wrap:
        self.data.load(fn, **kw)
        return self

    def get_index(self) -> np.ndarray:
        return np.array(list(self.data.index))

    def get_label(self) -> str:
        return ', '.join(self.data.label)

    def get_value(self) -> np.ndarray:
        return np.array(list(flatten(self.data.value)))

    def get_color(self) -> str:
        return self.plot[0].get_color()
