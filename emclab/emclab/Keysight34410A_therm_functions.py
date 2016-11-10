import numpy as np
import time
from emclab import Keysight34410A

def set_therm():
    therm = Keysight34410A(7)
    therm.temp_meas_set('rtd', 4)

    return therm
