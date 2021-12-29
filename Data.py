from __future__ import annotations
from   typing   import Any, Iterable, Union

import numpy  as np
import pandas as pd

from . import Misc


__all__ = ['Data', 'fmt_float']


def fmt_float(_: int, cs: str) -> list[float]:
    return list(map(float, cs.split()))


class Data(object):

    class Lut(object):

        def __init__(self, a: list[list[str]]):
            rev = [1]
            for n in reversed(list(map(len, a))):
                rev.append(rev[-1] * n)

            self.tot = rev[-1]
            self.arr = [(n, {s: i for i, s in enumerate(r)}) for r, n in zip(a, reversed(rev[:-1]))]

        def __call__(self, key: tuple[Union[str, list[str]]]) -> list[int]:
            rev = [0]

            for (n, d), k in reversed(list(zip(self.arr, key + ('', ) * len(self.arr)))):
                acc = []
                for i in (d if not k else [k] if isinstance(k, str) else k):
                    o = n * d[i]
                    acc.extend(map(lambda x: x + o, rev))
                rev = sorted(acc)

            return rev

    def __init__(self):
        self.rows = []
        self.cols = []
        self.data = []
        self.rlut = None
        self.clut = None
        self.df   = None

    def __getattr__(self, k: str) -> Any:
        if k == 'T':
            if self.df is None:
                raise AttributeError(k)

            self.df              = self.df.T
            self.rows, self.cols = self.cols, self.rows
            self.rlut, self.clut = self.clut, self.rlut

            return self
        else:
            raise AttributeError(k)

    def __getitem__(self, k: Any) -> Data:
        def loc(c: Any, d: Data.Lut, recur: int = 0) -> list[int]:
            # fail-fast
            if isinstance(c, int):
                return [c]
            if isinstance(c, str):
                return d((c, ))
            if isinstance(c, tuple):
                return d(c)
            if recur:
                raise KeyError(k)
            if isinstance(c, list):
                return list(Misc.flatten(map(lambda x: loc(x, d, 1), c)))
            if isinstance(c, slice):
                if c.start is None and c.stop is None:
                    return list(range(0,
                                      d.tot,
                                      Misc.identity(c.step, 1)))
                return list(range(loc(c.start, d, 1)[0],
                                  loc(c.stop,  d, 1)[0],
                                      Misc.identity(c.step, 1)))
            raise KeyError(k)

        if isinstance(k, tuple):
            return Data().wrap(self.df.iloc[loc(k[0], self.rlut), loc(k[1], self.clut)])
        else:
            return Data().wrap(self.df.iloc[loc(k,    self.rlut)])

    def add_rows(self, *rs: str, **kw: Any) -> Data:
        if kw.get('auto', None):
            self.rows.append(list(map(str, range(len(self.data) // int(np.prod(list(map(len, self.cols))))))))
        else:
            self.rows.append(list(rs))
        return self

    def add_cols(self, *cs: str, **kw: Any) -> Data:
        if kw.get('auto', None):
            self.cols.append(list(map(str, range(len(self.data) // int(np.prod(list(map(len, self.rows))))))))
        else:
            self.cols.append(list(cs))
        return self

    def add_data(self, *ds: Union[Any, list[Any]], **kw: Any) -> Data:
        if ((fn := kw.get('file', None)) and
            (fc := kw.get('func', None))):
            with open(fn) as fd:
                for i, cs in enumerate(fd):
                    self.data.extend(fc(i, cs))
        else:
            self.data.extend(Misc.flatten(ds))
        return self

    def raw_data(self, *ds: list[Any]) -> Data:
        if not ds:
            return self
        return self.wrap(pd.DataFrame(np.array(ds),
                                      index   = pd.MultiIndex.from_product([list(map(str, range(len(ds   ))))]),
                                      columns = pd.MultiIndex.from_product([list(map(str, range(len(ds[0]))))])))

    def wrap(self, df: pd.DataFrame):
        def rex(mi: pd.Index) -> list[list[str]]:
            raw = list(zip(*[i for i in mi]))
            ret = [[]          for _ in range(len(raw))]

            for prw, prt in zip(raw, ret):
                dic = set()
                for r in prw:
                    if r not in dic:
                        dic.add(r)
                        prt.append(r)
            return ret

        self.df   = df
        self.rows = rex(self.df.index)
        self.cols = rex(self.df.columns)
        self.rlut = Data.Lut(self.rows)
        self.clut = Data.Lut(self.cols)
        return self

    def save(self, fn: str) -> Data:
        self.df.to_pickle(fn)
        return self

    def load(self, fn: str, **kw: Any) -> Data:
        return self.wrap(pd.read_pickle(fn, **kw))

    def done(self, **kw: Any) -> Misc.Wrap:
        if self.df is None:
            self.rlut = Data.Lut(self.rows)
            self.clut = Data.Lut(self.cols)
            self.df   = pd.DataFrame(np.array(self.data).reshape((self.rlut.tot,
                                                                  self.clut.tot)),
                                     index   = pd.MultiIndex.from_product(self.rows),
                                     columns = pd.MultiIndex.from_product(self.cols))

        return Misc.Wrap(self, **kw)

    @property
    def index(self) -> np.ndarray:
        return self.df.index

    @property
    def label(self) -> str:
        return self.df.columns[0]

    @property
    def value(self) -> np.ndarray:
        return self.df.values
