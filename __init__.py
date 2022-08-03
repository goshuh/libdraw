from __future__ import annotations

from .Data import *
from .Path import *
from .Draw import *
from .Wrap import *
from .Ext  import *


def init() -> None:
    import pandas            as pd
    import matplotlib.pyplot as pl

    # rainbow color
    # see: https://loading.io/color/feature/Rainbow/
    rainbow = ['#4355db',
               '#34bbe6',
#              '#49da9a',
               '#a3e048',
               '#f7d038',
               '#eb7532',
               '#e6261f',
               '#d23be7']

    # global
    pl.rcParams['figure.figsize' ] = (10, 6)
    pl.rcParams['font.family'    ] = 'Cantarell'
    pl.rcParams['font.size'      ] =  20
    pl.rcParams['axes.prop_cycle'] =  pl.cycler(color = rainbow)

    # print all the data
    pd.set_option('display.max_rows',     None)
    pd.set_option('display.max_columns',  None)
    pd.set_option('display.width',        None)
    pd.set_option('display.max_colwidth', None)


init()
