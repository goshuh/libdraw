from __future__ import annotations
from   typing   import Any, Iterator, Union

import numpy  as np
import pandas as pd


__all__ = ['Data']


class Data(object):

    @staticmethod
    def flat(*ds: Any) -> Iterator[Any]:
        for d in ds:
            if isinstance(d, (list, tuple, np.ndarray, pd.Index)):
                yield from Data.flat(*d)
            else:
                yield d

    @staticmethod
    def read(_: int, cs: str) -> list[float]:
        def cov(s: str) -> float:
            try:
                return float(s)
            except Exception:
                return float('nan')
        return list(map(cov, cs.split()))

    class Lut(object):

        def __init__(self, ss: list[list[str]]):
            rev = [1]

            for n in reversed(list(map(len, ss))):
                rev.append(rev[-1] * n)

            self.tot = rev[-1]
            self.arr = [(n, {r: i for i, r in enumerate(s)}) for s, n in zip(ss, reversed(rev[:-1]))]

        def __call__(self, ks: tuple[Union[str, list[str]]]) -> list[int]:
            rev = [0]

            for (n, d), k in reversed(list(zip(self.arr, ks + ('', ) * len(self.arr)))):
                acc = []
                for i in (d if not k else [k] if isinstance(k, str) else k):
                    o = n * d[i]
                    acc.extend(map(lambda x: x + o, rev))
                rev = sorted(acc)

            return rev

    def __init__(self, **kw):
        r = kw.get('rows')
        c = kw.get('cols')

        self._rows    = [list(r)] if r else []
        self._cols    = [list(c)] if c else []
        self._raw     = []
        self._row_lut = None
        self._col_lut = None
        self._data    = None

        self.data(**kw)

    def __getattr__(self, k: str) -> Any:
        if k == 'T':
            if self._data is None:
                raise AttributeError(k)

            self._data                   = self._data.T
            self._rows,    self._cols    = self._cols,    self._rows
            self._row_lut, self._col_lut = self._col_lut, self._row_lut

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
                return list(Data.flat(map(lambda x: loc(x, d, 1), c)))
            if isinstance(c, slice):
                if c.start is None and c.stop is None:
                    return list(range(0,
                                      d.tot,
                                      c.step if c.step else 1))
                return list(range(loc(c.start, d, 1)[0],
                                  loc(c.stop,  d, 1)[0],
                                      c.step if c.step else 1))
            raise KeyError(k)

        if isinstance(k, tuple):
            return Data().wrap(self._data.iloc[loc(k[0], self._row_lut), loc(k[1], self._col_lut)])
        else:
            return Data().wrap(self._data.iloc[loc(k,    self._row_lut)])

    def rows(self, *rs: str, **kw: Any) -> Data:
        if kw.get('auto'):
            self._rows.append(list(map(str, range(len(self._raw) // int(np.prod(list(map(len, self._cols))))))))
        else:
            self._rows.append(list(Data.flat(rs)))

        return self

    def cols(self, *cs: str, **kw: Any) -> Data:
        if kw.get('auto'):
            self._cols.append(list(map(str, range(len(self._raw) // int(np.prod(list(map(len, self._rows))))))))
        else:
            self._cols.append(list(Data.flat(cs)))

        return self

    def data(self, *ds: Union[Any, list[Any]], **kw: Any) -> Data:
        if fn := kw.get('file'):
            with open(fn) as fd:
                fc = kw.get('func', Data.read)
                for i, cs in enumerate(fd):
                    self._raw.extend(fc(i, cs))
        elif ds:
            self._raw.extend(list(Data.flat(ds)))

        return self

    def done(self) -> Data:
        if not self._rows and not self._cols:
            raise ValueError(self)

        if not self._cols:
            self.cols(auto = True)
        if not self._rows:
            self.rows(auto = True)
        if not self._data:
            self._row_lut = Data.Lut(self._rows)
            self._col_lut = Data.Lut(self._cols)
            self._data    = pd.DataFrame(np.array(self._raw).reshape((self._row_lut.tot,
                                                                      self._col_lut.tot)),
                                         index   = pd.MultiIndex.from_product(self._rows),
                                         columns = pd.MultiIndex.from_product(self._cols))

        return self

    def load(self, fn: str, **kw: Any) -> Data:
        return self.wrap(pd.read_pickle(fn, **kw))

    def save(self, fn: str) -> Data:
        self._data.to_pickle(fn)
        return self

    def wrap(self, df: pd.DataFrame) -> Data:
        def rev(mi: pd.Index) -> list[list[str]]:
            raw = list(zip(*[i for i in mi]))
            ret = [[]          for _ in range(len(raw))]

            for prw, prt in zip(raw, ret):
                dic = set()
                for r in prw:
                    if r not in dic:
                        dic.add(r)
                        prt.append(r)

            return ret

        self._data    = df
        self._rows    = rev(self._data.index)
        self._cols    = rev(self._data.columns)
        self._row_lut = Data.Lut(self._rows)
        self._col_lut = Data.Lut(self._cols)

        return self

    def unwrap(self) -> pd.DataFrame:
        def one(mi: pd.Index) -> list[str]:
            return [i[0] for i in mi]

        if self._data is None:
            self.done()

        data       = self._data
        self._data = None

        # TODO
        if data.index  .nlevels == 1:
            data.index   = pd.Index(one(data.index))
        if data.columns.nlevels == 1:
            data.columns = pd.Index(one(data.columns))

        return data
