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
                 ['PHASE_NOISE', 'dBc/Hz']]

    _special_vars = ['T_STAMP', 'T_ADD']
    _special_vars_legacy = ['TIMESTAMP', 'ADDING_TIME']
    _special_units = ['s', 's']
    _just = 9

    #===============================================================
    def __init__(self, meas_vars = None):
        """Initialization.

        Input parameters
        ----------------
        meas_vars: List of [var_name, var_unit] lists.
        If given, the matrix is initialized using meas_vars.
        If None, the matrix is initialized using DataCollector._meas_vars.
        """

        # use copy
        meas_vars = deepcopy(meas_vars)

        # user-defined measured variables
        if meas_vars is None:
            meas_vars = self._meas_vars

        # add special vars if not already present
        names = [mm[0] for mm in meas_vars]
        for legacy, special_var, special_unit in zip(self._special_vars_legacy,
                                                     self._special_vars,
                                                     self._special_units):
            if legacy not in names and \
               special_var not in names:
                meas_vars.append([special_var, special_unit])

        # rename legacy names if present
        for legacy, special_var, special_unit in zip(self._special_vars_legacy,
                                                     self._special_vars,
                                                     self._special_units):
            if legacy in names:
                index = names.index(legacy)
                meas_vars[index][0] = special_var

        # build index of variables and units
        self._vars = dict()
        self._units = dict()
        for i, (var, unit) in enumerate(meas_vars):
            self._vars[var] = i
            self._units[var] = unit

        # define header
        self.header = ','.join([var + " [" + unit + "]"
                                for var, unit in meas_vars])

        # define header for human-readable output
        self.header_h = '\t'.join([(var + " [" + unit + "]").rjust(self._just)
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

        # list containing the number of entries in the meas lists
            # 1 represents a scalar
        numel = list()
        for key in meas.data.keys():
            try:
                # case 2
                numel.append(len(meas.data[key]))
            except TypeError:
                # case 1
                numel.append(1)

        # get number of list entries and check data consistency
            # all entries should be either scalars, or lists of equal length
        N = max(numel)
        if not all([val in [0, N] for val in numel]):
            raise ValueError("Data inconsistent!")

        # define the new rows
        new_data = np.ones((N, len(self._vars)))

        for param, col in self._vars.items():
            if param in meas.data.keys():
                new_data[:, col] *= meas.data[param]
            elif param not in self._special_vars:
                new_data[:, col] *= np.nan

        # calculate the timestamp and adding time
        new_data[:, self._vars['T_STAMP']] *= meas.time_out
        new_data[:, self._vars['T_ADD']] *= meas.time_out - meas.time_in

        # append new row to matrix
        self.matrix = np.vstack((self.matrix, new_data))

        # output human readable progress log
        np.savetxt("PROGRESS_LOG.txt", self.matrix,
                   fmt = '%' + str(self._just) + '.3g',
                   delimiter = '\t', header = self.header_h)

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
