# -*- coding: utf-8 -*-
import numpy as np
import time
from nose.tools import *

from ..Measurement import *
from ..DataCollector import *

#===============================================================
def test_Measurement_add():
    """Measurement.add()

    """

    # test cases:
        # TC1 - add several measurements within several seconds

    time_in = time.time()

    # define new Measurement object
    meas = Measurement()
    meas.add('VDD', 3.3)
    time.sleep(3)
    meas.add('AVDD', 3.3)
    time.sleep(2)
    meas.add('IB', 10e-6)

    time_out = time.time()

    # check timing
    assert np.isclose(meas.time_in, time_in, atol = 0.1, rtol = 0)
    assert np.isclose(meas.time_out, time_out, atol = 0.1, rtol = 0)
    deltaT = meas.time_out - meas.time_in
    assert np.isclose(deltaT, 5, atol = 0.1, rtol = 0)
