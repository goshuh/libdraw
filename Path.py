from __future__ import annotations

from . import Data
from . import Misc


class Axis(object):

    def __init__(self, n: str, g: bool = False):
        self.name = n
        self.log  = g
        self.data = []
        self.canv = []
        self.diff = []

    def __call__(self, c: float) -> float:
        r = (c - self.canv[0]) / self.diff[0]
        if self.log:
            return self.data[0] * self.diff[1] ** r
        else:
            return self.data[0] + self.diff[1] *  r

    def corr(self, d: float, c: float) -> Axis:
        self.data.append(d)
        self.canv.append(c)

        if len(self.canv) == 2:
            self.diff.append(self.canv[1] - self.canv[0])
            self.diff.append(self.data[1] / self.data[0] if self.log else
                             self.data[1] - self.data[0])
        return self


class Path(object):

    def __init__(self, x: Axis, y: Axis, *data, **kw):
        self.x = x
        self.y = y
        self.d = []

        raw = []
        if ((fn := kw.get('file', None)) and
            (fc := kw.get('func', None))):
            with open(fn) as fd:
                for i, cs in enumerate(fd):
                    raw.extend(fc(i, cs))
        else:
            raw = data

        for a, b in zip(raw[0::2], raw[1::2]):
            self.d.append(x(a))
            self.d.append(y(b))

    def done(self, **kw) -> Misc.Wrap:
        return (Data.Data()
                    .add_cols(self.x.name, self.y.name)
                    .add_data(self.d)
                    .add_rows(auto = True)
                    .done(**kw))
