import numpy as np
import time

#===============================================================
class DataCollector(object):
    """Data Collector.

    """
    #===============================================================
    def __init__(self):
        """Initialization. Creates a dictionary.

        """
        self.data = dict()

    #===============================================================
    def add(self, meas):
        """Add content to the dictionary.

        Input parameters
        ----------------
        meas: add a measurement to the dictionary

        """
        lista_avdd = list()
        lista_i_avdd = list()
        lista_vdd = list()
        lista_i_vdd = list()
        lista_vref = list()
        lista_i_ref = list()
        lista_i_b = list()
        lista_ron = list()
        lista_temp = list()
        lista_freq = list()
        lista_pssr = list()
        lista_phase_noise = list()
        lista_timestamp = list()
        lista_timestamp_s = list()

        print("\nPOCETAK\n")

        for key, value in self.data.items():
            if key == 'AVDD':
                if self.data['AVDD'] != []:
                    for v in value:
                        lista_avdd.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'I_AVDD':
                if self.data['I_AVDD'] != []:
                    for v in value:
                        lista_i_avdd.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'VDD':
                if self.data['VDD'] != []:
                    for v in value:
                        lista_vdd.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'I_VDD':
                if self.data['I_VDD'] != []:
                    for v in value:
                        lista_i_vdd.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'VREF':
                if self.data['VREF'] != []:
                    for v in value:
                        lista_vref.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'I_REF':
                if self.data['I_REF'] != []:
                    for v in value:
                        lista_i_ref.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'I_B':
                if self.data['I_B'] != []:
                    for v in value:
                        lista_i_b.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'RON':
                if self.data['RON'] != []:
                    for v in value:
                        lista_ron.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'TEMP':
                if self.data['TEMP'] != []:
                    for v in value:
                        lista_temp.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'FREQ':
                if self.data['FREQ'] != []:
                    for v in value:
                        lista_freq.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'PSSR':
                if self.data['PSSR'] != []:
                    for v in value:
                        lista_pssr.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'PHASE_NOISE':
                if self.data['PHASE_NOISE'] != []:
                    for v in value:
                        lista_phase_noise.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'TIMESTAMP':
                if self.data['TIMESTAMP'] != []:
                    for v in value:
                        lista_timestamp.append(float(str(v).replace('[', '').replace(']', '')))
            if key == 'TIMESTAMP_S':
                if self.data['TIMESTAMP_S'] != []:
                    for v in value:
                        lista_timestamp_s.append(float(str(v).replace('[', '').replace(']', '')))
        for key, value in meas.data.items():
            if key == 'AVDD':
                if meas.data['AVDD'] != []:
                    lista_avdd.append(value)
                elif meas.data['AVDD'] == []:
                    lista_avdd.append(0.0)
            if key == 'I_AVDD':
                if meas.data['I_AVDD'] != []:
                    lista_i_avdd.append(value)
                elif meas.data['I_AVDD'] == []:
                    lista_i_avdd.append(0.0)
            if key == 'VDD':
                if meas.data['VDD'] != []:
                    lista_vdd.append(value)
                elif meas.data['VDD'] == []:
                    lista_vdd.append(0.0)
            if key == 'I_VDD':
                if meas.data['I_VDD'] != []:
                    lista_i_vdd.append(value)
                elif meas.data['I_VDD'] == []:
                    lista_i_vdd.append(0.0)
            if key == 'VREF':
                if meas.data['VREF'] != []:
                    lista_vref.append(value)
                elif meas.data['VREF'] == []:
                    lista_vref.append(0.0)
            if key == 'I_REF':
                if meas.data['I_REF'] != []:
                    lista_i_ref.append(value)
                elif meas.data['I_REF'] == []:
                    lista_i_ref.append(0.0)
            if key == 'I_B':
                if meas.data['I_B'] != []:
                    lista_i_b.append(value)
                elif meas.data['I_B'] == []:
                    lista_i_b.append(0.0)
            if key == 'RON':
                if meas.data['RON'] != []:
                    lista_ron.append(value)
                elif meas.data['RON'] == []:
                    lista_ron.append(0.0)
            if key == 'TEMP':
                if meas.data['TEMP'] != []:
                    lista_temp.append(value)
                elif meas.data['TEMP'] == []:
                    lista_temp.append(0.0)
            if key == 'FREQ':
                if meas.data['FREQ'] != []:
                    lista_freq.append(value)
                elif meas.data['FREQ'] == []:
                    lista_freq.append(0.0)
            if key == 'PSSR':
                if meas.data['PSSR'] != []:
                    lista_pssr.append(value)
                elif meas.data['PSSR'] == []:
                    lista_pssr.append(0.0)
            if key == 'PHASE_NOISE':
                if meas.data['PHASE_NOISE'] != []:
                    lista_phase_noise.append(value)
                elif meas.data['PHASE_NOISE'] == []:
                    lista_phase_noise.append(.00)
            if key == 'TIMESTAMP':
                if meas.data['TIMESTAMP'] != []:
                    lista_timestamp.append(value)
                elif meas.data['TIMESTAMP'] == []:
                    lista_timestamp.append(0.0)

        lista_timestamp_s.append(meas.time)

        self.data.clear()
        print(self.data)

        self.data['AVDD'] = lista_avdd
        self.data['I_AVDD'] = lista_i_avdd
        self.data['VDD'] = lista_vdd
        self.data['I_VDD'] = lista_i_vdd
        self.data['VREF'] = lista_vref
        self.data['I_REF'] = lista_i_ref
        self.data['I_B'] = lista_i_b
        self.data['RON'] = lista_ron
        self.data['TEMP'] = lista_temp
        self.data['FREQ'] = lista_freq
        self.data['PSSR'] = lista_pssr
        self.data['PHASE_NOISE'] = lista_phase_noise
        self.data['TIMESTAMP'] = lista_timestamp
        self.data['TIMESTAMP_S'] = lista_timestamp_s

        print(self.data)
