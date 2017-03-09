import numpy as np
import time
from emclab import Keysight53220A

def set_freqm(ratio = None, gatetime = None):
    clk1 = Keysight53220A(1, 1, gatetime = gatetime)
    clk2 = Keysight53220A(1, 2, gatetime = gatetime)
    bd1 = Keysight53220A(2, 1, gatetime = gatetime)
    bd2 = Keysight53220A(2, 2, gatetime = gatetime)
    list_of_fm = [clk1, clk2, bd1, bd2]

    return list_of_fm

def meas_freqm(fm):
    freqm = list()
    freqm.append(fm[0].meas_freq_r())
    freqm.append(fm[1].meas_freq_r())
    freqm.append(fm[2].meas_width_r())
    freqm.append(fm[3].meas_width_r())

    return freqm
