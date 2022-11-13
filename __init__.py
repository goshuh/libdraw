from .Data import *
from .Draw import *


def init():
    import proplot as pp

    pp.rc_matplotlib[ 'figure.dpi'] = 72
    pp.rc_matplotlib['savefig.dpi'] = 72

    pp.rc['subplots.refwidth'] =  8
    pp.rc['font.name'        ] = 'Calibri'
    pp.rc['font.size'        ] =  24
    pp.rc['image.cmap'       ] = 'gnuplot'
    pp.rc['legend.frameon'   ] =  False


init()
