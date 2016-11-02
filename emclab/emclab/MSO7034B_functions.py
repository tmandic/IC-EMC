import numpy as np
import time
from emclab import MSO7034B

def set_freqm1():
    clk1 = MSO7034B('0x0957::0x173D::MY50340261', 1)
    clk2 = MSO7034B('0x0957::0x173D::MY50340261', 2)
    bd1 = MSO7034B('0x0957::0x173D::MY50340261', 3)
    bd2 = MSO7034B('0x0957::0x173D::MY50340261', 4)
    list_of_fm = [clk1, clk2, bd1, bd2]

    return list_of_fm

def meas_freqm1(fm):
    freqm = list()
    freqm.append(fm[0].meas_freq())
    freqm.append(fm[1].meas_freq())
    freqm.append(fm[2].pwidth)
    freqm.append(fm[3].pwidth)

    return freqm
