import numpy as np
import os
import time

#===============================================================
class DataCollector(object):
    """Data Collector.

    """

    # list of measured variables with units
    _meas_vars = [['AVDD', 'V'],
                 ['I_AVDD', 'A'],
                 ['VDD', 'V'],
                 ['I_VDD', 'A'],
                 ['VREF', 'V'],
                 ['IREF', 'A'],
                 ['V_IREF', 'V'],
                 ['IB', 'A'],
                 ['RON', 'V'],
                 ['PD', 'A'],
                 ['TEMP', 'C'],
                 ['FREQ', 'Hz'],
                 ['SENSITIVITY', 'Hz/V'],
                 ['PHASE_NOISE', 'dBc/Hz'],
                 ['TIMESTAMP', ''],
                 ['ADDING_TIME', 's']]

    # build index of variables and units
    vars = dict()
    units = dict()
    for i, (var, unit) in enumerate(_meas_vars):
        vars[var] = i
        units[var] = unit

    # define header
    header = ','.join([var + " [" + unit + "]"
                           for var, unit in _meas_vars])

    #===============================================================
    def __init__(self):
        """Initialization.

        """

        ncol = len(self.vars)
        self.matrix = np.array([]).reshape(0, ncol)

    #===============================================================
    def add(self, meas):
        """Add new measurement to the matrix.

        Input parameters
        ----------------
        meas: a Measurement object.
        """

        new_data = np.zeros(len(self.vars))

        for param, ind in self.vars.items():
            if param in meas.data:
                new_data[ind] = meas.data[param]
            else:
                new_data[ind] = np.nan

        # calculate the timestamp and adding time
        new_data[self.vars['TIMESTAMP']] = meas.time_out
        new_data[self.vars['ADDING_TIME']] = meas.time_out - meas.time_in

        # append new row to matrix
        self.matrix = np.vstack((self.matrix, new_data))

    #===============================================================
    def save(self, fname):
        """Output data to file.

        fname: filename for the output file.

        Note
        ----
        The human readable file is also output with the "_h" extension.
        """

        # create output directory if it does not exist
        output_dir = os.path.dirname(fname)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # output CSV
        np.savetxt(fname + ".csv",
                   self.matrix, delimiter = ",", header = self.header)

        # output human readable
        matrix_h = self._get_human_readable()
        np.savetxt(fname + "_h.csv",
                   matrix_h, delimiter = ",", header = self.header)

    #===============================================================
    # PRIVATE METHODS
    #===============================================================
    def _get_human_readable(self):
        """Return human readable version of self.matrix.

        Not implemented.
        """

        return self.matrix
