# -*- coding: utf-8 -*-
import numpy as np
import time
import os
from nose.tools import *

from .__init__ import __file__ as root
from ..Measurement import *
from ..DataCollector import *

#===============================================================
def test_DataCollector_add():
    """DataCollector.add()

    """

    # test cases:
        # TC1 - add measurements to matrix

    # define current directory using relative import
    cd = os.path.dirname(root)

    # create the test folder
    test_dir = cd + "/files.testdata"

    # define new DataCollector object
    data = DataCollector()

    # define new Measurement object
    meas = Measurement()
    meas.add('VDD', 3.3)
    time.sleep(0.3)
    meas.add('AVDD', 3.3)
    time.sleep(0.8)
    meas.add('IB', 10e-6)

    # add measurement to data collector
    data.add(meas)

    data.save(test_dir + "/test")

    print(data.matrix)
    assert False
