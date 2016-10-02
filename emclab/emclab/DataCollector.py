import numpy as np
import os
import time

#===============================================================
class DataCollector(object):
    """Data Collector.

    """

    # index connecting parameters to matrix columns
    index = {
        'AVDD'          : 0,
        'I_AVDD'        : 1,
        'VDD'           : 2,
        'I_VDD'         : 3,
        'VREF'          : 4,
        'I_REF'         : 5,
        'V_IREF'        : 6,
        'IB'            : 7,
        'RON'           : 8,
        'PD'            : 9,
        'TEMP'          : 10,
        'FREQ'          : 11,
        'PSRR'          : 12,
        'PHASE_NOISE'   : 13,
        'TIMESTAMP'     : 14,
        'ADDING_TIME'   : 15,
    }

    # define header
    header = 'AVDD [V],' + \
             'I_AVDD [A],' + \
             'VDD [V],' + \
             'I_VDD [A],' + \
             'VREF [V],' + \
             'I_REF [A],' + \
             'V_IREF [V],' + \
             'IB [A],' + \
             'RON [V],' + \
             'PD [V],' + \
             'TEMP [C],' + \
             'FREQ [Hz],' + \
             'PSRR [Hz/V],' + \
             'PHASE_NOISE,' + \
             'TIMESTAMP [sse],' + \
             'ADDING_TIME [s]'

    #===============================================================
    def __init__(self):
        """Initialization.

        """

        ncol = len(self.index)
        self.matrix = np.array([]).reshape(0, ncol)

    #===============================================================
    def add(self, meas):
        """Add new measurement to the matrix.

        Input parameters
        ----------------
        meas: a Measurement object.
        """

        new_data = np.zeros(len(self.index))

        for param, ind in self.index.items():
            if param in meas.data:
                new_data[ind] = meas.data[param]
            else:
                new_data[ind] = np.nan

        # calculate the timestamp and adding time
        new_data[self.index['TIMESTAMP']] = meas.time_out
        new_data[self.index['ADDING_TIME']] = meas.time_out - meas.time_in

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
