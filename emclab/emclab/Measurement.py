import numpy as np
import time

#===============================================================
class Measurement(object):
    """Measurement.

    """
    #===============================================================
    def __init__(self):
        """Initialization.

        """

        self.data = dict()
        self.time_in = None
        self.error = ''

    #===============================================================
    def add(self, parameter, data):
        """Add content to the dictionary.

        Input parameters
        ----------------
        parameter: what parameter to write in (keyword)
        data: data assigned to the previously specified keyword

        """

        # update time of the first added measurement
        if self.time_in is None:
            self.time_in = time.time()

        # update time of the last added measurement
        self.time_out = time.time()

        # parse through the data
            # case 1: data is a scalar
            # case 2: data is a list
            # case 3: data is a dict
        try:
            # case 3: find the error key (should be only one)
            non_empty_keys = [key for key, val in data.items() if val]
            assert len(non_empty_keys) == 1
            key = non_empty_keys[0]

            # collect the data
            self.data[parameter] = data[key]

            # store the error
            self.error += key
        except AttributeError:
            # cases 1, 2
            self.data[parameter] = data

    #===============================================================
