# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

defaults = {
    'scale'             : None,
    'sizing'            : 42,
    'legend_sizing'     : 29,
    'figsize'           : [24, 12.85],
    'linewidth'         : 5,
    'markersize'        : 15,
    'markeredge'        : 5,
    'gridwidth'         : 1.5,
    'xtick_pad'         : 15,
    'ytick_pad'         : 15,
    'frame_width'       : 2.0,
    'font'              : 'Times New Roman',
    'axisbelow'         : True,
    'use_switch'        : False,
    'grid'              : True,
    'grid_which'        : 'both',
    'grid_linestyle'    : '-',
    'gridcolor'         : (0.486, 0.486, 0.486),
    'dpi'               : 300,
    'ftype'             : "png",

    'leg'               : 'off',
    'leg_r'             : 'off',
    'leg_d'             : 'off',
    'leg_cols'          : 1,
    'leg_r_cols'        : 1,
    'leg_d_cols'        : 1,
}

# class attribute defaults
class Vals(object):
    def __init__(self, defaults):
        self.__dict__.update(defaults)

vals = Vals(defaults)

def emclab_axes():
    # define the misc parameters
    plt.rcParams['font.family'] = vals.font
    plt.rcParams['font.size'] = vals.sizing
    plt.rcParams['savefig.dpi'] = int(vals.dpi)

    # define the axes and grid properties
    plt.rcParams['axes.linewidth'] = vals.frame_width
    plt.rcParams['axes.labelsize'] = vals.sizing
    plt.rcParams['axes.titlesize'] = vals.sizing
    plt.rcParams['axes.axisbelow'] = vals.axisbelow
    plt.rcParams['axes.grid'] = vals.grid
    plt.rcParams['axes.grid.which'] = vals.grid_which
    plt.rcParams['grid.linestyle'] = vals.grid_linestyle
    plt.rcParams['grid.linewidth'] = vals.gridwidth
    plt.rcParams['grid.color'] = vals.gridcolor
    plt.rcParams['xtick.labelsize'] = vals.sizing
    plt.rcParams['ytick.labelsize'] = vals.sizing
    plt.rcParams['xtick.major.pad'] = str(vals.xtick_pad)
    plt.rcParams['ytick.major.pad'] = str(vals.ytick_pad)

    # define the line properties
    plt.rcParams['lines.linewidth'] = vals.linewidth
    plt.rcParams['lines.markersize'] = vals.markersize
    plt.rcParams['lines.markeredgewidth'] = vals.markeredge

    # define the legend properties
    plt.rcParams['legend.fontsize'] = vals.legend_sizing
    plt.rcParams['legend.handlelength'] = 3
    plt.rcParams['legend.numpoints'] = 1
    plt.rcParams['legend.loc'] = 'lower left'
    plt.rcParams['legend.borderaxespad'] = 0

    # define figure size
    plt.rcParams['figure.figsize'] = vals.figsize

    # transform text attributes in tuples if necessary
    try:
        vals.text.title()
        if vals.text is not None:
            vals.text = (vals.text, )
            vals.text_loc = (vals.text_loc, )
    except AttributeError:
        pass
