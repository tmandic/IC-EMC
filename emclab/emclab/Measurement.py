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

        self.data[parameter] = data

    #===============================================================
    def add_list(self, parameter, data):
        # update time of the first added measurement
        if self.time_in is None:
            self.time_in = time.time()

        # update time of the last added measurement
        self.time_out = time.time()

        self.data[parameter] = data
