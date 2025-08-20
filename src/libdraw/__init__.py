import os

from .Data import Data
from .Draw import Draw


def init():
    import cycler
    import pandas    as pd
    import ultraplot as up

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

    cycle = up.Cycle(
        color     = palette,
        marker    = markers,
        linewidth = 2)

    pd.set_option('display.max_columns',       None)
    pd.set_option('display.max_rows',          None)
    pd.set_option('display.max_colwidth',      None)
    pd.set_option('display.expand_frame_repr', None)

    up.rc_matplotlib['figure.dpi'             ] =  72
    up.rc_matplotlib['figure.max_open_warning'] =  False
    up.rc_matplotlib['savefig.dpi'            ] =  72
    up.rc_matplotlib['svg.fonttype'           ] = 'none'

    # use the bundle font
    fd = os.path.join(os.path.dirname(__file__), 'fonts')

    up.register_fonts(os.path.join(fd, 'LinLibertine_RBIah.ttf',
                      os.path.join(fd, 'LinLibertine_RBah.ttf',
                      os.path.join(fd, 'LinLibertine_RIah.ttf',
                      os.path.join(fd, 'LinLibertine_RZIah.ttf',
                      os.path.join(fd, 'LinLibertine_RZah.ttf',
                      os.path.join(fd, 'LinLibertine_Rah.ttf')

    up.rc['cmap'                ] = 'gnuplot'
    up.rc['axes.prop_cycle'     ] =  cycle
    up.rc['font.name'           ] = 'Linux Libertine'
    up.rc['font.size'           ] =  20
    up.rc['title.loc'           ] = 'uc'
    up.rc['title.size'          ] =  20
    up.rc['grid'                ] =  False
    up.rc['gridminor'           ] =  False
    up.rc['lines.markersize'    ] =  8
    up.rc['legend.fontsize'     ] =  20
    up.rc['legend.frameon'      ] =  False
    up.rc['legend.columnspacing'] =  1
    up.rc['subplots.refwidth'   ] =  6


init()
