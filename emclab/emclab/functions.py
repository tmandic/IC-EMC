import numpy as np
import time
from emclab import KeysightE3649A

def set_all():
    fnam = enter_fname()

    itera = iterations()

    inst1, dev1 = init_dev(1, fnam)
    inst2, dev2 = init_dev(2, fnam)
    inst3, dev3 = init_dev(3, fnam)

    set_volt(inst1, dev1)
    set_volt(inst2, dev2)
    set_volt(inst3, dev3)

    matrix1 = meas_volt(inst1, dev1, itera)
    matrix2 = meas_volt(inst2, dev2, itera, matrix1)
    matrix3 = meas_volt(inst3, dev3, itera, matrix2)

    data = make_data_matrix(matrix3)
    return data

def enter_fname():
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
        adress = 5
        inst = KeysightE3649A(adress, fname)
    elif dev == 2:
        adress = 5
        inst = KeysightE3649A(adress, fname)
    elif dev == 3:
        adress = 6
        inst = KeysightE3649A(adress, fname)
    else:
        raise ValueError("Please enter a valid input\n")
    return inst, dev

def set_volt(inst, dev = None):
    if dev == None:
        dev = int(input("1 - VDD\n2 - AVDD\n3 - VREF\n"))
    if dev == 1:
        channel = 1
        inst.set_both(1, 3.3, 0.4)
    elif dev == 2:
        channel = 2
        inst.set_both(2, 3.3, 0.4)
    elif dev == 3:
        channel = 1
        inst.set_both(1, 1.2, 0.3)
    else:
        raise ValueError("Please enter a valid input\n")

def iterations():
    itera = int(input("Number of iterations: "))
    return itera

def meas_volt(inst, dev, itera, input_matrix = None):
    if input_matrix == None:
        iterat = itera
        matrix = np.zeros((int(iterat), 13))
    else:
        matrix = input_matrix
        iterat = len(matrix)

##    matrix = matrix.astype('|S16')

    if dev == 1:
        column = 2
        channel = 1
    elif dev == 2:
        column = 0
        channel = 2
    elif dev == 3:
        column = 4
        channel = 1
    else:
        raise ValueError("Please enter a valid input\n")

    for i in range(int(iterat)):
        matrix[:, column] = inst.voltage(channel)
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
