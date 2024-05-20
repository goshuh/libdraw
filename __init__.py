from .Data import Data
from .Draw import Draw


def init():
    import cycler
    import pandas  as pd
    import proplot as pp

    # https://github.com/easystats/see/blob/HEAD/R/scale_color_okabeito.R
    palette = [
        '#E69F00',
        '#009E73',
        '#0072B2',
        '#D55E00',
        '#CC79A7',
        '#000000',
        '#56B4E9',
        '#009E73',
        '#D55E00',
        '#CC79A7',
        '#F5C710',
        '#F5C710'
    ]

    pd.set_option('display.max_columns',       None)
    pd.set_option('display.max_rows',          None)
    pd.set_option('display.max_colwidth',      None)
    pd.set_option('display.expand_frame_repr', None)

    pp.rc_matplotlib['figure.dpi'             ] = 72
    pp.rc_matplotlib['figure.max_open_warning'] = False
    pp.rc_matplotlib['savefig.dpi'            ] = 72

    pp.rc['cmap'             ] = 'gnuplot'
    pp.rc['axes.prop_cycle'  ] =  pp.Cycle(c = palette, lw = 2)
    pp.rc['font.name'        ] = 'Calibri'
    pp.rc['font.size'        ] =  16
    pp.rc['grid'             ] =  False
    pp.rc['gridminor'        ] =  False
    pp.rc['legend.fontsize'  ] =  16
    pp.rc['legend.frameon'   ] =  False
    pp.rc['subplots.refwidth'] =  6


init()
