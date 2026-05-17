from .Data import Data
from .Draw import Draw


# nebula colors
palette_nebula = [
    '#000000',
    '#307098',
    '#832211',
    '#b26925'
]

palette_nebula_more = [
    '#307098',
    '#365937',
    '#b26925',
    '#832211',
    '#aa4499',
    '#000000'
]

# https://github.com/easystats/see/blob/HEAD/R/scale_color_okabeito.R
palette_okabeito = [
    '#E69F00',
    '#009E73',
    '#0072B2',
    '#D55E00',
    '#CC79A7',
    '#F5C710'
]

# https://github.com/Gnuplotting/gnuplot-palettes
palette_rdylbu = [
    '#4575b4',
    '#74add1',
    '#abd9e9',
#   '#e0f3f8',
#   '#fee090',
    '#fdae61',
    '#f46d43',
    '#d73027'
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

hatches = [
    '//',
   r'\\',
    '++',
    'oo',
    '..'
]


def set_cycle(ax = None, **kw):
    import ultraplot as up

    c = up.Cycle(color     = kw.get('color',  palette_nebula),
                 marker    = kw.get('marker', markers),
                 linewidth = 2)

    if ax:
        ax.set_prop_cycle(c)
    else:
        up.rc['axes.prop_cycle'] = c


def scale_v(c, f):
    import matplotlib.colors as mc

    hsv = mc.rgb_to_hsv(mc.to_rgb(c))
    hsv[2] *= f
    return mc.hsv_to_rgb(hsv)


def scale_b(c, f):
    import numpy             as np
    import matplotlib.colors as mc

    rgb = np.array(mc.to_rgb(c))
    return rgb + ([1, 1, 1] - rgb) * f


def _init():
    import os
    import pandas    as pd
    import ultraplot as up

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

    up.register_fonts(os.path.join(fd, 'LinLibertine_RBIah.ttf'),
                      os.path.join(fd, 'LinLibertine_RBah.ttf' ),
                      os.path.join(fd, 'LinLibertine_RIah.ttf' ),
                      os.path.join(fd, 'LinLibertine_RZIah.ttf'),
                      os.path.join(fd, 'LinLibertine_RZah.ttf' ),
                      os.path.join(fd, 'LinLibertine_Rah.ttf'  ))

    up.rc['cmap'                ] = 'gnuplot'
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

    set_cycle()


_init()
