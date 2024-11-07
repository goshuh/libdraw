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
        '#F5C710'
    ]

    # nebula colors
    palette = [
        '#000000',
        '#307098',
        '#832211',
        '#b26925'
    ]

    markers = [
        'o',
        'v',
        '^',
        's',
        'p',
        'h',
        'd'
    ]

    cycle = pp.Cycle(
        c         = palette,
        marker    = markers,
        linewidth = 2)

    pd.set_option('display.max_columns',       None)
    pd.set_option('display.max_rows',          None)
    pd.set_option('display.max_colwidth',      None)
    pd.set_option('display.expand_frame_repr', None)

    pp.rc_matplotlib['figure.dpi'             ] = 72
    pp.rc_matplotlib['figure.max_open_warning'] = False
    pp.rc_matplotlib['savefig.dpi'            ] = 72

    pp.rc['cmap'                ] = 'gnuplot'
    pp.rc['axes.prop_cycle'     ] =  cycle
    pp.rc['font.name'           ] = 'Times New Roman'
    pp.rc['font.size'           ] =  20
    pp.rc['title.loc'           ] = 'uc'
    pp.rc['title.size'          ] =  20
    pp.rc['grid'                ] =  False
    pp.rc['gridminor'           ] =  False
    pp.rc['lines.markersize'    ] =  8
    pp.rc['legend.fontsize'     ] =  20
    pp.rc['legend.frameon'      ] =  False
    pp.rc['legend.columnspacing'] =  1
    pp.rc['subplots.refwidth'   ] =  6


init()
