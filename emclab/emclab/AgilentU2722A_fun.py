import numpy as np
import time
from emclab import AgilentU2722A

#smu 1, channel 1, iref
params_ch1 = {
    'addr'              : '0x0957::0x4118::MY56380004',
    'fname'             : 'smu_log',
    'channum'           : 1,
    'sourcemode'        : 'I',
    'vlimit'            : 3.3,
    'vrange'            : '20V',
    'ilimit'            : 1e-4,
    'irange'            : '100u',
    'outval'            : 10e-6
}

#smu 1, channel 2, ib
params_ch2 = {
    'addr'              : '0x0957::0x4118::MY56380004',
    'fname'             : 'smu_log',
    'channum'           : 2,
    'sourcemode'        : 'I',
    'vlimit'            : 3.3,
    'vrange'            : '20V',
    'ilimit'            : 1e-5,
    'irange'            : '10u',
    'outval'            : 5e-6
}

#smu 1, channel 3, vref
params_ch3 = {
    'addr'              : '0x0957::0x4118::MY56380004',
    'fname'             : 'smu_log',
    'channum'           : 3,
    'sourcemode'        : 'V',
    'vlimit'            : 1.5,
    'vrange'            : '2V',
    'ilimit'            : 0.1,
    'irange'            : '120m',
    'outval'            : 1.2
}

#smu 2, channel 1, ron
params_ron = {
    'addr'              : '0x0957::0x4118::MY56400004',
    'fname'             : 'smu_log',
    'channum'           : 1,
    'sourcemode'        : 'V',
    'vlimit'            : 5,
    'vrange'            : '20V',
    'ilimit'            : 0.1,
    'irange'            : '120m',
    'outval'            : 0
}

params = [params_ch1, params_ch2, params_ch3, params_ron]

def set_smu(iref = None, ib = None, vref = None, ron = None):
    """Sets up Agilent U2722A.

    Returns channels.

    Input parameters
    ----------------
    (OPTIONAL - if nothing is entered, AgilentU2722A will be set to default values listed below.

    iref - sets up the channel 1 (IREF) current output of the SMU1
    (float number) - the curent will be set to this number [A]
    'def', 'default', 'DEF', 'DEFAULT' - the current will be set to 10e-6
    (the maximum current that can be set is 100u)

    ib - sets up the channel 2 (IB) current output of the SMU1
    (float number) - the current will be set to this number [A]
    'def', 'default', 'DEF', 'DEFAULT' - the voltage will be set to 5e-6
    (the maximum current that can be set is 10u)

    vref - sets up the channel 3 (VREF) voltage output of the SMU1
    (float number) - the voltage will be set to this number [V]
    'def', 'default', 'DEF', 'DEFAULT' - the voltage will be set to 1.2
    (the maximum voltage that can be set is 2)

    ron - sets up the channel 1 (RON) voltage output of the SMU2
    (float number) - the voltage will be set to this number [V]
    'def', 'default', 'DEF', 'DEFAULT' - the voltage will be set to 0
    (the maximum voltage that can be set is 5)

    IMPORTANT: if any of the these channels is set, others will be set to their default values

    """
    insts = list()

    if iref != None:
        if iref not in ['def', 'default', 'DEF', 'DEFAULT']:
            params[0]['outval'] = iref
    if ib != None:
        if ib not in ['def', 'default', 'DEF', 'DEFAULT']:
            params[1]['outval'] = ib
    if vref != None:
        if vref not in ['def', 'default', 'DEF', 'DEFAULT']:
            params[2]['outval'] = vref
    if ron != None:
        if ron not in ['def', 'default', 'DEF', 'DEFAULT']:
            params[3]['outval'] = ron

    for i in range(4):
        inst = AgilentU2722A(params[i]['addr'], params[i]['channum'])
        inst.volt_limit(params[i]['vlimit'])
        inst.volt_range(params[i]['vrange'])
        inst.curr_limit(params[i]['ilimit'])
        inst.curr_range(params[i]['irange'])
        inst.tinterval(1)
        if params[i]['sourcemode'] == 'I':
            inst.curr_out(params[i]['outval'])
        elif params[i]['sourcemode'] == 'V':
            inst.volt_out(params[i]['outval'])
        else:
            raise ValueError("Error.\n")
        insts.append(inst)

    for i in range(4):
        insts[i].output(1)

    return insts

def meas_smu(insts):
    voltm = list()
    currm = list()
    for inst in insts:
        voltm.append(inst.meas(1))
        currm.append(inst.meas(2))

    return voltm, currm
