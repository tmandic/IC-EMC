import numpy as np
from emclab import KeysightE3649A

def set_volt(dev = None):
    if dev == None:
        dev = int(input("1 - VDD\n2 - AVDD\n3 - VREF\n"))
    if dev == 1:
        channel = 1
        adress = 5
        inst = KeysightE3649A(adress)
        inst.set_both(1, 3.3, 0.3)
    elif dev == 2:
        channel = 2
        adress = 5
        inst = KeysightE3649A(adress)
        inst.set_both(2, 3.3, 0.3)
    elif dev == 3:
        channel = 1
        adress = 6
        inst = KeysightE3649A(adress)
        inst.set_both(1, 1.2, 0.2)
    else:
        raise ValueError("Please enter a valid input\n")
    return inst, dev

def meas_volt(inst, dev, input_matrix = None):
    itera = int(input("Number of iterations?\n"))
    global matrix
    if input_matrix == None:
        matrix = np.zeros((int(itera), 13))
    else:
        matrix = input_matrix
    items = ["AVDD", "I_AVDD", "VDD", "I_VDD",
            "VREF", "I_REF", "I_B", "RON",
            "TEMP", "FREQ", "PSSR",
            "PHASE_NOISE", "TIME"]
    header = ','.join(items)
    meas_volt_loop(inst, dev, itera, matrix)
    fname="meas_volt.csv"
    np.savetxt(fname, matrix, delimiter = ",", header = header)
    data_in = np.genfromtxt(fname, delimiter = ",", names = True)

    return data_in

def meas_volt_loop(inst, dev, itera, matrix):

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

    for i in range(int(itera)):
        matrix[:, column] = inst.voltage(channel)

    return matrix
