import numpy as np
import time
from emclab import KeysightE3649A

def set_vdd(fname = None, iterb = None):
    fnam = enter_fname(fname = fname)

    itera = iterations(iterb = iterb)

    VDD = init_dev(1, fnam)

    return VDD, itera

def turnon_vdd(VDD, itera):
    set_volt(VDD)

    matrix1 = meas_volt(VDD, itera)

    data = make_data_matrix(matrix1)

    return data

def enter_fname(fname = None):
    if fname == None:
        fname = input("Filename: ")
    return fname

def init_dev(dev = None, fnam = None):
    if fnam == None:
        fname = enter_fname()
    else:
        fname = fnam
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

def iterations(iterb = None):
    if iterb == None:
        iterb = int(input("Number of iterations: "))
    return iterb

def meas_volt(inst, itera, input_matrix = None):
    if input_matrix == None:
        iterat = itera
        matrix = np.zeros((int(iterat), 13))
    else:
        matrix = input_matrix
        iterat = len(matrix)

##    matrix = matrix.astype('|S16')

    if (inst.addr == 5) and (inst.chan == 1):
        column = 2
    elif (inst.addr == 5) and (inst.chan == 2):
        column = 0
    elif (inst.addr == 6) and (inst.chan == 1):
        column = 4
    else:
        raise ValueError("Please enter a valid input\n")

    for i in range(int(iterat)):
        matrix[:, column] = inst.voltage()
        matrix[:, 12] = inst.time_float
    return matrix

def make_data_matrix(matrix):
    items = ["AVDD", "I_AVDD", "VDD", "I_VDD",
            "VREF", "I_REF", "I_B", "RON",
            "TEMP", "FREQ", "PSSR",
            "PHASE_NOISE", "TIME"]
    header = ','.join(items)
    fname="meas_volt.csv"
##    np.savetxt(fname, matrix, delimiter = ",", header = header, fmt="%s")
    np.savetxt(fname, matrix, delimiter = ",", header = header)
    data_in = np.genfromtxt(fname, delimiter = ",", names = True)

    return data_in
