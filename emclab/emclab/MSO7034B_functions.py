import numpy as np
import time
from emclab import MSO7034B

def set_freqm():
    clk1 = MSO7034B('0x0957::0x173D::MY50340261', 1)
    clk2 = MSO7034B('0x0957::0x173D::MY50340261', 2)
    bd1 = MSO7034B('0x0957::0x173D::MY50340261', 3)
    bd2 = MSO7034B('0x0957::0x173D::MY50340261', 4)
    list_of_fm = [clk1, clk2, bd1, bd2]

    return list_of_fm

def meas_freqm(fm):
    freqm = dict()
    freqm['CLK1'] = fm[0].meas_freq()
    freqm['CLK2'] = fm[1].meas_freq()
    freqm['BD1'] = fm[2].meas_width(1)
    freqm['BD2'] = fm[3].meas_width(1)

    return freqm
