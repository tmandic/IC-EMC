import numpy as np
import time
from emclab import KeysightE3649A

#Keysight E3469A, adress 3, channel 1, VDD
params_kleft1 = {
    'addr'              : 3,
    'channel'           : 1,
    'fname'             : 'volt_log'
}

params_out_kleft1= {
    'volt'          : 3.3,
    'max_curr'      : 0.4
}

#Keysight E3469A, adress 3, channel 2, VCC
params_kleft2 = {
    'addr'              : 3,
    'channel'           : 2,
    'fname'             : 'volt_log'
}

params_out_kleft2 = {
    'volt'           : 3.3,
    'max_curr'       : 0.4
}

#Keysight E3469A, adress 6, channel 1
params_kright1 = {
    'addr'              : 6,
    'channel'           : 1,
    'fname'             : 'volt_log'
}

params_out_kright1= {
    'volt'          : 3.3,
    'max_curr'       : 0.4
}

#Keysight E3469A, adress 6, channel 2
params_kright2 = {
    'addr'              : 6,
    'channel'           : 2,
    'fname'             : 'volt_log'
}

params_out_kright2= {
    'volt'           : 1.2,
    'max_curr'       : 0.4
}

params = [params_kleft1, params_kleft2, params_kright1, params_kright2]
params_out = [params_out_kleft1, params_out_kleft2, params_out_kright1, params_out_kright2]

def set_volt(kleft1 = None, kleft2 = None, kright1 = None, kright2 = None):
    """Sets up Keysight E3649A instruments.

    Returns channels.

    Input parameters
    ----------------
    (OPTIONAL - if nothing is entered, only the left Keysight E3649A instrument
                on the left channel (adress 5, channel 1) will be set to 3.3V.

    kleft1 - sets up the voltage of the left Keysight E3649A instrument on the left channel (adress 5, channel 1).
    (float number) - the voltage will be set to this number
    'def', 'default', 'DEF', 'DEFAULT' - the voltage will be set to 3.3 V

    kleft2 - sets up the voltage of the left Keysight E3649A instrument on the right channel(adress 5, channel 2).
    (float number) - the voltage will be set to this number
    'def', 'default', 'DEF', 'DEFAULT' - the voltage will be set to 3.3 V

    kright1 - sets up the voltage of the right Keysight E3649A instrument on the left channel(adress 6, channel 1).
    (float number) - the voltage will be set to this number
    'def', 'default', 'DEF', 'DEFAULT' - the voltage will be set to 3.3 V

    kright2 - sets up the voltage of the right Keysight E3649A instrument on the right channel(adress 6, channel 21).
    (float number) - the voltage will be set to this number
    'def', 'default', 'DEF', 'DEFAULT' - the voltage will be set to 1.2 V

    The maximum current for any of these channels is set to 0.4 A.

    IMPORTANT: if any of the these voltages is set, kleft1 will not be set to 3.3 V
    (it too must be done manually by defining kleft1 = 3.3 in the arguments of set_volt)

    """
    counter = [0, 0, 0, 0]

    if kleft1 != None:
        if kleft1 not in ['def', 'default', 'DEF', 'DEFAULT']:
            params_out_kleft1['volt'] = kleft1
        counter[0] = 1
    if kleft2 != None:
        if kleft2 not in ['def', 'default', 'DEF', 'DEFAULT']:
            params_out_kleft2['volt'] = kleft2
        counter[1] = 1
    if kright1 != None:
        if kright1 not in ['def', 'default', 'DEF', 'DEFAULT']:
            params_out_kright1['volt'] = kright1
        counter[2] = 1
    if kright2 != None:
        if kright2 not in ['def', 'default', 'DEF', 'DEFAULT']:
            params_out_kright2['volt'] = kright2
        counter[3] = 1

    if sum(counter) == 0:
        kvolt = KeysightE3649A(**params_kleft1)
        kvolt.set_both(**params_out_kleft1)
    elif sum(counter) == 1:
        j = counter.index(1)
        kvolt = KeysightE3649A(**params[j])
        kvolt.set_both(**params_out[j])
    else:
        kvolt = list()
        for i in [i for i,x in enumerate(counter) if x == 1]:
            inst = KeysightE3649A(**params[i])
            kvolt.append(inst)
        j = 0
        for i in [i for i,x in enumerate(counter) if x == 1]:
            kvolt[j].set_both(**params_out[i])
            j = j + 1

    return kvolt

def meas_volt(kvolt):
    if isinstance(kvolt, list):
        kvoltm = list()
        for i in kvolt:
            kvoltm.append(i.voltage())
    else:
        kvoltm = kvolt.voltage()

    return kvoltm
