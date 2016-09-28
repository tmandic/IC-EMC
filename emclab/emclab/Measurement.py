import numpy as np
import time

#===============================================================
class Measurement(object):
    """Measurement.

    """
    #===============================================================
    def __init__(self, parameter, data):
        """Initialization. Creates a dictionary.

        Input parameters
        ----------------
        parameter: what parameter to write in (keyword)
        data: data assigned to the previously specified keyword

        """
        self.data = dict()
        self.data['AVDD'] = list()
        self.data['I_AVDD'] = list()
        self.data['VDD'] = list()
        self.data['I_VDD'] = list()
        self.data['VREF'] = list()
        self.data['I_REF'] = list()
        self.data['I_B'] = list()
        self.data['RON'] = list()
        self.data['TEMP'] = list()
        self.data['FREQ'] = list()
        self.data['PSSR'] = []
        self.data['PHASE_NOISE'] = list()
        self.data['TIMESTAMP'] = list()
        self.add(parameter, data)

    #===============================================================
    def add(self, parameter, data):
        """Add content to the dictionary.

        Input parameters
        ----------------
        parameter: what parameter to write in (keyword)
        data: data assigned to the previously specified keyword

        """
        if parameter.lower().startswith('avdd'):
            self.time = time.time()
            self.data['AVDD'] = data
        elif parameter.lower().startswith('i_avdd'):
            self.time = time.time()
            self.data['I_AVDD'] = data
        elif parameter.lower().startswith('vdd'):
            self.time = time.time()
            self.data['VDD'] = data
        elif parameter.lower().startswith('vdd'):
            self.time = time.time()
            self.data['VDD'] = data
        elif parameter.lower().startswith('i_vdd'):
            self.time = time.time()
            self.data['I_VDD'] = data
        elif parameter.lower().startswith('vref'):
            self.time = time.time()
            self.data['VREF'] = data
        elif parameter.lower().startswith('i_ref'):
            self.time = time.time()
            self.data['I_REF'] = data
        elif parameter.lower().startswith('i_b'):
            self.time = time.time()
            self.data['I_B'] = data
        elif parameter.lower().startswith('ron'):
            self.time = time.time()
            self.data['RON'] = data
        elif parameter.lower().startswith('temp'):
            self.time = time.time()
            self.data['TEMP'] = data
        elif parameter.lower().startswith('freq'):
            self.time = time.time()
            self.data['FREQ'] = data
        elif parameter.lower().startswith('pssr'):
            self.time = time.time()
            self.data['PSSR'] = data
        elif parameter.lower().startswith('phase_noise'):
            self.time = time.time()
            self.data['PHASE_NOISE'] = data
        elif parameter.lower().startswith('timestamp'):
            self.time = time.time()
            self.data['TIMESTAMP'] = self.time
        else:
            raise ValueError("Wrong input\n")
