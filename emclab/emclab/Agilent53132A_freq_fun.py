import numpy as np
import time
from emclab import Agilent53132A

def set_freqma():
    clk1 = Agilent53132A(13, 1)
    clk2 = Agilent53132A(13, 2)
    list_of_fm = [clk1, clk2]

    return list_of_fm

def meas_freqma(fm):
    freqm = list()
    freqm.append(fm[0].meas_freq())
    freqm.append(fm[1].meas_freq())

    return freqm
