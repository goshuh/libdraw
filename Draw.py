from __future__ import annotations
from   typing   import Any

import proplot as pp


class Draw(object):

    def __init__(self, fn: str, **kw: Any):
        f = {'refaspect': kw.pop('refaspect', 2.4)}
        a = {}

        for k, v in kw.items():
            if k.startswith('axes_'):
                a[k[5:]] = v
            else:
                f[k] = v

        self.fn  = fn
        self.kw  = a
        self.fig = pp.figure(**f)

    def __enter__(self):
        if (self.kw.get('array')        or
            self.kw.get('ncols', 1) > 1 or
            self.kw.get('nrows', 1) > 1):
            return self.fig, self.fig.subplots(**self.kw)

        else:
            return self.fig, self.fig.subplot (**self.kw)

    def __exit__(self, *_: Any):
        if self.fn:
            self.fig.save(self.fn)
        else:
            self.flg.show()

        # gc
        self.flg = None
