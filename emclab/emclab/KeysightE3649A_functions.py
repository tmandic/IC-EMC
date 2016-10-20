import numpy as np
import time
from emclab import KeysightE3649A

def set_vdd(fname = None):
    VDD = init_dev(1, fname)

    set_volt(VDD)

    return VDD

def init_dev(dev = None, fname = None):
    if dev == None:
        dev = int(input("1 - VDD\n2 - AVDD\n3 - VREF\n"))
    if dev == 1:
        inst = KeysightE3649A(5, 1, fname)
    elif dev == 2:
        inst = KeysightE3649A(5, 2, fname)
    elif dev == 3:
        inst = KeysightE3649A(6, 1, fname)
    else:
        raise ValueError("Please enter a valid input\n")
    return inst

def set_volt(inst):
    if (inst.addr == 5) and (inst.chan == 1):
        inst.set_both(3.3, 0.4)
    elif (inst.addr == 5) and (inst.chan == 2):
        inst.set_both(3.3, 0.4)
    elif (inst.addr == 6) and (inst.chan == 1):
        inst.set_both(1.2, 0.3)
    else:
        raise ValueError("Please enter a valid input\n")

def meas_vdd(inst, input_matrix = None):
    return inst.voltage()
