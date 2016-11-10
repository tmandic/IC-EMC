import numpy as np
import os
import time
from copy import deepcopy

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

    #===============================================================
    def __init__(self, meas_vars = None):
        """Initialization.

        Input parameters
        ----------------
        meas_vars: List of [var_name, var_unit] lists.
        If given, the matrix is initialized using meas_vars.
        If None, the matrix is initialized using DataCollector._meas_vars.
        """

        if meas_vars is None:
            meas_vars = self._meas_vars

        # build index of variables and units
        self._vars = dict()
        self._units = dict()
        for i, (var, unit) in enumerate(meas_vars):
            self._vars[var] = i
            self._units[var] = unit

        # define header
        self.header = ','.join([var + " [" + unit + "]"
                                for var, unit in meas_vars])

        ncol = len(self._vars)
        self.matrix = np.array([]).reshape(0, ncol)

    #===============================================================
    def add(self, meas):
        """Add new measurement to the matrix.

        Input parameters
        ----------------
        meas: a Measurement object.

        Notes
        -----
        If meas contains lists of N entries, appends the N measurements to
        the last N measurements in the matrix.
        Raises ValueError if data with no column is encountered.
        Raises ValueError if all data for all keys in meas is not the same length.
        Raises ValueError if self.matrix is too short for list data.
        """

        # make a copy of meas
        meas = deepcopy(meas)

        # check if all data keys are in self._vars.keys()
        error = False
        for key in meas.data.keys():
            if key not in self._vars.keys():
                print("'" + key + "' not defined in DataCollector!")
                error = True
        if error:
            raise ValueError("Some measured data not defined in DataCollector!")

        # parse through the data
            # case 1: meas contains only scalars
            # case 2: meas contains lists of equal length

        # list containing the number of entries in the meas lists
        # 0 represents a scalar
        numel = list()
        for key in meas.data.keys():
            try:
                # case 2
                numel.append(len(meas.data[key]))
            except TypeError:
                # case 1
                numel.append(0)

##        # check data consistency
##        if not all([val == numel[0] for val in numel]):
##            raise ValueError("Data inconsistent!")

        # get number of list entries (or 0 for scalar case)
        N = numel[0]

        if not N:
            # define the new row
            new_data = np.zeros(len(self._vars))

            for param, col in self._vars.items():
                if param in meas.data.keys():
                    new_data[col] = meas.data[param]
                else:
                    new_data[col] = np.nan

            # calculate the timestamp and adding time
            new_data[self._vars['TIMESTAMP']] = meas.time_out
            new_data[self._vars['ADDING_TIME']] = meas.time_out - meas.time_in

            # append new row to matrix
            self.matrix = np.vstack((self.matrix, new_data))

        else:
            # append data to the N last rows
##            if len(self.matrix) < N:
##                raise ValueError("Cannot append data to matrix!")
            # if all data does not have the same length, crop the first entries
            N_crop = min(numel)
            for key in meas.data.keys():
                meas.data[key] = meas.data[key][-N_crop:]

            N_add = min(len(self.matrix), N)

            # parse through the data
            for key in meas.data.keys():
                col = self._vars[key]
                self.matrix[-N_add:, col] = meas.data[key][:N_add]

            # check error message
            if meas.error:
                self.header = meas.error + "\n" + self.header

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
        if output_dir and not os.path.exists(output_dir):
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
