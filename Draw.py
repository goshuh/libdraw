from __future__ import annotations
from   typing   import Any, Callable, Union

import numpy                 as np
import matplotlib.pyplot     as pl
import matplotlib.lines      as ml
import matplotlib.transforms as mt
import matplotlib.figure     as mf
import matplotlib.axes       as ma

from . import Misc


__all__ = ['Draw']


class Draw(object):

    def __init__(self, *a: Any, **kw: Any):
        self.fig, self.ax = pl.subplots(*a, **kw)
        self.axs  = [self.ax]
        # hack
        self.ax.int_all  = []
        self.ax.int_tick = None

    def add(self, misc: ml.Artist):
        misc.set_in_layout(True)
        self.ax.add_artist(misc)

    def draw_2sf(self, i: int, n: int, d: Misc.Wrap) -> None:
        d.x     = d.get_index()
        d.y     = d.get_value()
        d.label = Misc.identity(d.label, d.get_label())

        self.ax.int_all.append(d)
        self.ax.int_tick = Misc.identity(self.ax.int_tick, d)

        if Misc.valid(d.tick):
            self.ax.int_tick = d

        if Misc.valid(d.bar):
            if i == 0 or Misc.valid(d.tick):
                self.ax.int_tick = d.set_bar_acc(np.zeros(len(d.x)))

            wid = Misc.identity(self.ax.int_tick.wid, 0.6) / n
            shf = wid * (i - 0.5 * (n - 1))
            d.bar_pos = np.arange(len(d.x)) + shf
            d.bar_wid = wid

            d.plot = self.ax.bar (d.bar_pos, d.y, d.bar_wid,
                                  label  = d.label,
                                  color  = d.color,
                                  bottom = self.ax.int_tick.bar_acc)
            self.ax.int_tick.bar_acc += d.y

        if Misc.valid(d.line):
            d.plot = self.ax.plot(np.arange(len(d.x)), d.y, Misc.identity(d.style, ''),
                                  label     = d.label,
                                  color     = d.color,
                                  linewidth = d.wid)

        if Misc.valid(d.xticklabels_idx):
            d.x = list(map(lambda x: [x[d.xticklabels_idx]], d.x))

    def draw_2ff(self, _: int, __: int, d: Misc.Wrap) -> None:
        v = d.get_value()

        d.x     = np.array(v[0::2])
        d.y     = np.array(v[1::2])
        d.label = Misc.identity(d.label, d.get_label())

        self.ax.int_all.append(d)
        self.ax.int_tick = Misc.identity(self.ax.int_tick, d)

        if Misc.valid(d.line):
            d.plot = self.ax.plot(d.x, d.y, Misc.identity(d.style, ''),
                                  label     = d.label,
                                  color     = d.color,
                                  linewidth = d.wid)
        if Misc.valid(d.mark):
            d.plot = self.ax.plot(d.x, d.y, Misc.identity(d.style, '') + 'o',
                                  label     = d.label,
                                  color     = d.color)

    def draw_cat(self, *ds: Any) -> Union[np.ndarray, list]:
        if not ds or len(ds[0]) == 1:
            return np.array(list(Misc.flatten(ds)))

        m   = len(ds)
        n   = len(ds[0])
        cur = ['' for _ in range(n)]
        cmd = [[] for _ in range(n)]

        for i, d in enumerate(ds):
            upd = False
            for j in range(n):
                if upd or cur[j] != d[j]:
                    cmd[j].append((not upd, i - 0.5, d[j]))
                    cur[j] = d[j]
                    upd    = True

        # sentry
        for i in range(n):
            cmd[i].append((i == 0, m - 0.5, ''))
            cmd[i].append((False,      0.0, ''))

        # ad-hoc things
        wid = ml.rcParams['xtick.major.width']
        ext = ml.rcParams['font.size'        ] / 72.0 * wid
        pad = ext / 2.0
        dif = ext * 1.35
        xtr = self.ax.get_xaxis_transform()

        for i, c in enumerate(cmd):
            xd = []
            sz = pad + dif * (n - i - 1)
            # x: data + dpi(0.0), y: axes + dpi(offs)
            tr = xtr + mt.ScaledTranslation(0.0, -sz, self.fig.dpi_scale_trans)

            for (v, xl, t), (_, xr, _) in zip(c[:-1], c[1:]):
                if v:
                    xd.append(xl)
                if t:
                    self.add(self.ax.text(0.5 * (xl + xr), 0.0, t,
                                          transform =  tr,
                                          ha        = 'center',
                                          va        = 'top'))

            # x: data, y: axes(0), show mark instead of line
            self.add(self.ax.add_line(pl.Line2D(xd, [0.0] * len(xd),
                                      transform       =  xtr,
                                      clip_on         =  False,
                                      linestyle       = 'none',
                                      marker          =  ml.TICKDOWN,
                                      markersize      =  72.0 * (sz + ext),
                                      markeredgecolor = 'black',
                                      markeredgewidth =  wid)))
        return []

    def twin(self) -> Draw:
        self.ax = self.axs[0].twinx()
        self.axs.append(self.ax)
        # hack
        self.ax.int_all  = []
        self.ax.int_tick = None
        # not working?
        self.ax.__dict__['_get_lines'].set_prop_cycle(self.axs[0].__dict__['_get_lines'].prop_cycler)

        return self

    def draw(self, *ds: Union[Misc.Wrap, list[Any]], show: bool = False) -> Draw:
        ds = list(Misc.flatten(ds))
        dn = len (ds)
        for i, d in enumerate(ds):
            if show:
                print(d.data.df)
            getattr(self, f'draw_{d.format}')(i, dn, d)
        return self

    def post(self, fc: Callable[[mf.Figure, ma.Axes], Any]) -> Draw:
        fc(self.fig, self.ax)
        return self

    def done(self, fn: str = '', **kw: Any) -> None:
        def fmt(x: float, _):
            return f'{x:g}'

        def loc(x: int):
            tr = {0:  2, # upper  left
                  1:  9, # upper  center
                  2:  1, # upper  right
                  3:  6, # center left
                  4: 10, # center
                  5:  7, # center right
                  6:  3, # lower  left
                  7:  8, # lower  center
                  8:  4} # lower  right
            return tr.get(x, 0) # best

        for ax in self.axs:
            d = ax.int_tick

            if d.title:
                ax.set_title(d.title)
            if d.xlabel:
                ax.set_xlabel(d.xlabel)
            if d.ylabel:
                ax.set_ylabel(d.ylabel)
            if Misc.valid(d.xlog):
                ax.set_xscale('log')
                if Misc.valid(d.xlog_fmt):
                    ax.xaxis.set_major_formatter(fmt)
            if Misc.valid(d.ylog):
                ax.set_yscale('log')
                if Misc.valid(d.ylog_real):
                    ax.yaxis.set_majot_formatter(fmt)
            if Misc.valid(d.xmin) or Misc.valid(d.xmax):
                ax.set_xlim(xmin = d.xmin,
                            xmax = d.xmax)
            if Misc.valid(d.ymin) or Misc.valid(d.ymax):
                ax.set_ylim(ymin = d.ymin,
                            ymax = d.ymax)

            if d.format == '2sf' and not Misc.identity(d.xticks_auto, False):
                # magic: draw lines before setting xticks
                xl = self.draw_cat(*d.x)
                ax.set_xticks     (np.arange(len(d.x)))
                ax.set_xticklabels(xl,
                                   fontsize = d.xtick_font,
                                   rotation = d.xtick_rot)
            else:
                if d.xticks:
                    ax.set_xticks([], minor = True)
                    ax.set_xticks(np.array(d.xticks))
                    if d.format == '2ff':
                        ax.set_xticklabels(list(map(str, d.xticks)))
                if d.xticklabels:
                    ax.set_xticklabels(np.array(d.xticklabels))

            if (leg := len(list(filter(lambda x: x.label, ax.int_all)))) > 1:
                ax.legend(loc            = loc(d.legend_loc),
                          ncol           = round(leg / Misc.identity(d.legend_row, leg)),
                          fontsize       = d.legend_font,
                          bbox_to_anchor = d.legend_bbox,
                          bbox_transform = self.fig.transFigure)

        if Misc.valid(fs := kw.get('figure_size', None)):
            self.fig.set_size_inches(*fs)
        if fn:
            pl.savefig(fn,
                       bbox_inches = 'tight',
                       transparent =  Misc.valid(kw.get('transparent', None)))

        pl.close()
