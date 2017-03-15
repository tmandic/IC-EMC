# -*- coding: utf-8 -*-
import numpy as np
import time
import os
from nose.tools import *
from pprint import pprint

from .__init__ import __file__ as root
from ..Measurement import *
from ..DataCollector import *

#===============================================================
def test_DataCollector_add():
    """DataCollector.add()

    """

    # test cases:
        # TC1 - add scalar measurements to matrix
        # TC2 - add list measurements to matrix

    # define current directory using relative import
    cd = os.path.dirname(root)

    # create the test folder
    test_dir = cd + "/files.testdata"

    #===============================================================
    # TC1
    #===============================================================
    # define new DataCollector object
    meas_vars = [['VDD', 'V'],
                 ['AVDD', 'V'],
                 ['TEMP', 'degC'],
                 ['FREQ', 'Hz']]
    dc = DataCollector(meas_vars)

    # make several measurements
    for i in range(10):
        meas = Measurement()
        meas.add('VDD', 3.3)
        time.sleep(0.03)
        meas.add('TEMP', 27)
        time.sleep(0.08)
        meas.add('FREQ', 1e6)

        # add measurement to data collector
        dc.add(meas)
    dc.save(test_dir + "/test_TC1")

    # load the data
    data = np.genfromtxt(test_dir + "/test_TC1.csv", names = True, delimiter = ",")
    assert data['VDD_V'].tolist() == [3.3] * 10
    assert data['TEMP_degC'].tolist() == [27] * 10
    assert data['FREQ_Hz'].tolist() == [1e6] * 10
    assert all([np.isnan(val) for val in data['AVDD_V']])

    #===============================================================
    # TC2
    #===============================================================
    # define new DataCollector object
    meas_vars = [['VDD', 'V'],
                 ['TEMP', 'degC'],
                 ['FREQ', 'Hz'],
                 ['TIMESTAMP', 's'],
                 ['ADDING_TIME', 's']]
    dc = DataCollector(meas_vars)

    # make several measurements
    for i in range(10):
        meas = Measurement()
        meas.add('VDD', 3.3)
        time.sleep(0.03)
        meas.add('TEMP', 27)
        time.sleep(0.08)
        meas.add('FREQ', [1e6])

        # add measurement to data collector
        dc.add(meas)
    dc.save(test_dir + "/test_TC2")

    # load the data
    data = np.genfromtxt(test_dir + "/test_TC1.csv", names = True, delimiter = ",")
    assert data['VDD_V'].tolist() == [3.3] * 10
    assert data['TEMP_degC'].tolist() == [27] * 10
    assert data['FREQ_Hz'].tolist() == [1e6] * 10
