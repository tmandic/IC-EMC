import numpy as np
import time
from emclab import KeysightE3649A

def set_all():
    fnam = enter_fname()

    itera = iterations()

    inst1 = init_dev(1, fnam)
    inst2 = init_dev(2, fnam)
    inst3 = init_dev(3, fnam)

    set_volt(inst1)
    set_volt(inst2)
    set_volt(inst3)

    matrix1 = meas_volt(inst1, itera)
    matrix2 = meas_volt(inst2, itera, matrix1)
    matrix3 = meas_volt(inst3, itera, matrix2)

    data = make_data_matrix(matrix3)

    print("x")
    inst2.voltage()
    print("x")
    inst3.voltage()
    print("x")
    inst1.voltage()
    print("x")
    print(inst1.addr)
    print("x")
    print(inst3.addr)
    print("x")
    print(inst2.chan)
    print("x")
    print(inst3.chan)
    print("x")

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

def iterations():
    itera = int(input("Number of iterations: "))
    return itera

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

#===============================================================
def timestamp():
    """Creates a timestamp both in float and string format

    Returns the created timestamp.

    """
    time_float = time.time()
    t0 = time.asctime(time.localtime(time_float))
    print(t0)
    t1 = t0[4:]
    t2=[]
    for t in t1:
        t2.append(t)
    if t1.startswith('Jan'):
        t3 = t2[4:]
        t3.insert(0, '1')
        t3.insert(0, '0')
    elif t1.startswith('Feb'):
        t3 = t2[4:]
        t3.insert(0, '2')
        t3.insert(0, '0')
    elif t1.startswith('Mar'):
        t3 = t2[4:]
        t3.insert(0, '3')
        t3.insert(0, '0')
    elif t1.startswith('Apr'):
        t3 = t2[4:]
        t3.insert(0, '4')
        t3.insert(0, '0')
    elif t1.startswith('May'):
        t3 = t2[4:]
        t3.insert(0, '5')
        t3.insert(0, '0')
    elif t1.startswith('Jun'):
        t3 = t2[4:]
        t3.insert(0, '6')
        t3.insert(0, '0')
    elif t1.startswith('Jul'):
        t3 = t2[4:]
        t3.insert(0, '7')
        t3.insert(0, '0')
    elif t1.startswith('Aug'):
        t3 = t2[4:]
        t3.insert(0, '8')
        t3.insert(0, '0')
    elif t1.startswith('Sep'):
        t3 = t2[4:]
        t3.insert(0, '9')
        t3.insert(0, '0')
    elif t1.startswith('Oct'):
        t3 = t2[4:]
        t3.insert(0, '0')
        t3.insert(0, '1')
    elif t1.startswith('Nov'):
        t3 = t2[4:]
        t3.insert(0, '1')
        t3.insert(0, '1')
    elif t1.startswith('Dec'):
        t3 = t2[4:]
        t3.insert(0, '2')
        t3.insert(0, '1')
    else:
        raise ValueError("Wrong date\n")
    day = t3[2:4]
    day.append('_')
    if day[0] == ' ':
        day[0] = '0'
    month = t3[0:2]
    month.append('_')
    year = t3[14:18]
    year.append('_')
    handm = t3[5:10]
    t4 = day + month + year + handm
    timestr=''.join(t4)
    self.time = timestr
    return timestr
