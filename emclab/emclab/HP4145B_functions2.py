from emclab import HP4145B_functions
from .HP4145B_functions import *

#smu channel 1, const i
params_IREF = {
    'addr'              : 16,
    'fname'             : 'spa_proba',
    'cd'                : 'smu',
    'channum'           : 1,
    'vname'             : 'VIREF',
    'iname'             : 'IREF',
    'sourcefunction'    : 'CONST',
    'sourcemode'        : 'I'
}

params_hp_IREF = {
    'compval'       : 3.3,
    'outval'        : 10e-6
}

#smu channel 2, const i
params_IB = {
    'addr'              : 16,
    'fname'             : 'spa_proba',
    'cd'                : 'smu',
    'channum'           : 2,
    'vname'             : 'VIB',
    'iname'             : 'IB',
    'sourcefunction'    : 'CONST',
    'sourcemode'        : 'I'
}

params_hp_IB = {
    'compval'       : 3.3,
    'outval'        : 5e-6
}

#smu channel 3, const i
params_IPT100 = {
    'addr'              : 16,
    'fname'             : 'spa_proba',
    'cd'                : 'smu',
    'channum'           : 3,
    'vname'             : 'VPT100',
    'iname'             : 'IPT100',
    'sourcefunction'    : 'CONST',
    'sourcemode'        : 'I'
}

params_hp_IPT100 = {
    'compval'       : 3.3,
    'outval'        : 1e-3
}

#smu channel 4, const v
params_VREF = {
    'addr'              : 16,
    'fname'             : 'spa_proba',
    'cd'                : 'smu',
    'channum'           : 4,
    'vname'             : 'VREF',
    'iname'             : 'IVREF',
    'sourcefunction'    : 'CONST',
    'sourcemode'        : 'V'
}

params_hp_VREF = {
    'compval'       : 0.1,
    'outval'        : 1.2
}


#a) smu channel vs1
params_ron0 = {
    'addr'              : 16,
    'fname'             : 'spa_proba',
    'cd'                : 'vs',
    'channum'           : 1,
    'vname'             : 'RON',
    'sourcefunction'    : 'CONST'
}

params_hp_ron0 = {
    'outval'        : 0
}

#b) smu channel vs1
params_ron1 = {
    'addr'              : 16,
    'fname'             : 'spa_proba',
    'cd'                : 'vs',
    'channum'           : 1,
    'vname'             : 'RON',
    'sourcefunction'    : 'CONST'
}

params_hp_ron1 = {
    'outval'        : 3.3
}

def set_spa(ron = None):
    if ron == None:
        ron = int(input("Enter 1 for RON turned on or 2 for RON turned off: "))

    if ron in ['0',0]:
        params_ron = params_ron0
        params_hp_ron = params_hp_ron0
    elif ron in ['1', 1]:
        params_ron = params_ron1
        params_hp_ron = params_hp_ron1

    iref, ib, ipt100, vref, ron = open_channels([params_IREF, params_IB, params_IPT100,
                                         params_VREF, params_ron])
    source_setup([iref, ib, ipt100, vref, ron], [params_hp_IREF, params_hp_IB, params_hp_IPT100,
                                         params_hp_VREF, params_hp_ron])

    list_of_hps = [iref, ib, ipt100, vref, ron]

    list_setup(list_of_hps)

    meas_setup(list_of_hps, 0.5, 3)

    return list_of_hps

def meas_spa(list_of_hps, me = None, osc = None, osc1 = None, osc2 = None):
    if me == None:
        raise ValueError("Please enter a valid input\n")
    meas = measure(list_of_hps, me, osc = osc, osc1 = osc1, osc2 = osc2)
    return meas

