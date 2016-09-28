# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class Keysight34410A(GPIB):
    """Digit multimeter Keysight 34410A.

    """
    #===============================================================
    def __init__(self, addr):
        """Initialization.

        """
        rm = visa.ResourceManager()
        self._dev = rm.open_resource('GPIB0::' + str(addr) + '::INSTR')

        # get instrument address

        self.addr = addr

        # get instrument name
        self.name = self._name()

    #===============================================================
    def get_address(self):
        """Get the device's address.

        """
        return self.addr

    #===============================================================
    def get_volt(self, acdc = None):
        """Measures voltage.

        Input parameters
        ----------------
        acdc: What signal to measure:
        direct current (1 or 'dc') or alternating current (2 or 'ac')

        """
        if acdc == None:
            acdc = int(input("Press 1 for DC voltage or 2 for AC voltage: \n"))

        if acdc in [1, 'dc']:
            u = float(self._dev.query('MEAS?'))
        elif acdc in [2, 'ac']:
            u = float(self._dev.query('MEAS:AC?'))
        else:
            raise ValueError("Error")
        print("The voltage is: ", u, "V.\n")
        return u

    #===============================================================
    def volt_range(self, acdc = None, rang = None):
        """Set or examine the voltage range.

        Input parameters
        ----------------
        acdc: What signal to measure:
        direct current (1 or 'dc') or alternating current (2 or 'ac')

        rang: determine the RANGE option of the multimeter
        0 or 'auto' for AUTO option;
        a number that will set the voltage range, choose between the following (in volts):
        0.1, 1, 10, 100, 1k (if another number is entered, the nearest one from
        the previously listed will be taken as the voltage range).

        """
        if acdc == None:
            acdc = int(input("Press 1 for DC voltage or 2 for AC voltage: "))

        if (acdc == 1) or (acdc == 'dc'):
            if rang == None:
                autotest = float(self._dev.query('VOLT:RANG:AUTO?'))
                rangetest = float(self._dev.query('VOLT:RANG?'))
                if autotest == 1:
                    print("DC voltage range is set to: AUTO.\n")
                else:
                    print("DC voltage range is set to: ", rangetest, "V.\n")
            elif (rang == 'auto') or  (rang == 0):
                self._dev.write('VOLT:RANG:AUTO ON')
                autotest = float(self._dev.query('VOLT:RANG:AUTO?'))
                if autotest == 1:
                    print("DC voltage range is set to: AUTO.\n")
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('VOLT:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('VOLT:RANG?'))
                print("DC voltage range is set to: ", rangetest, "V.\n")
        elif (acdc == 2) or (acdc == 'ac'):
            if rang == None:
                autotest = float(self._dev.query('VOLT:AC:RANG:AUTO?'))
                rangetest = float(self._dev.query('VOLT:AC:RANG?'))
                if autotest == 1:
                    print("AC voltage range is set to: AUTO.\n")
                else:
                    print("AC voltage range is set to: ", rangetest, "V.\n")
            elif (rang == 'auto') or  (rang == 0):
                self._dev.write('VOLT:AC:RANG:AUTO ON')
                autotest = float(self._dev.query('VOLT:AC:RANG:AUTO?'))
                if autotest == 1:
                    print("AC voltage range is set to: AUTO.\n")
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('VOLT:AC:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('VOLT:AC:RANG?'))
                print("AC voltage range is set to: ", rangetest, "V.\n")
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def volt_int(self, typ = None, val = None):
        """Set or examine the voltage INTEGRATION option of the multimeter.

        Input parameters
        ----------------
        typ: determine the INTEGRATION option of the multimeter
        1 or 'NPLC' or 'nplc' for NPLC; 2 or 'APERTURE' or 'aperture' for APERTURE;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the voltage range).

        val = time parameter needed to set NPLC or APERTURE mode;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the time parameter).

        """
        if typ == None:
            atest = float(self._dev.query('VOLT:APER:ENABLED?'))
            ntest = float(self._dev.query('VOLT:NPLC?'))
            if atest == 1:
                atest2 = float(self._dev.query('VOLT:APER?'))
                print("Voltage integration mode: APERTURE\nTime: ", atest2,"s.\n")
            else:
                print("Voltage integration mode: NPLC\nTime: ", ntest,"s.\n")
        elif (typ == 1) or (typ == 'NPLC') or (typ == 'nplc'):
            self._dev.write('VOLT:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('VOLT:NPLC?'))
            print("Voltage integration mode: NPLC\nTime: ", ntest,"s.\n")
        elif (typ == 2) or (typ == 'APERTURE') or (typ == 'aperture'):
            self._dev.write('VOLT:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('VOLT:APER?'))
            print("Voltage integration mode: APERTURE\nTime: ", atest2,"s.\n")
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================

    def get_curr(self, acdc):
        """Measures current.

        Input parameters
        ----------------
        acdc: What signal to measure:
        direct current (1 or 'dc') or alternating current (2 or 'ac')

        """
        if acdc == None:
            acdc = int(input("Press 1 for DC voltage or 2 for AC voltage: \n"))

        if acdc in [1, 'dc']:
            i = float(self._dev.query('MEAS:CURR?'))
        elif acdc in [2, 'ac']:
            i = float(self._dev.query('MEAS:CURR:AC?'))
        else:
            raise ValueError("Error")
        print("The current is: ", i, "A.\n")
        return i

    #===============================================================
    def curr_range(self, acdc = None, rang = None):
        """Set or examine the current range.

        Input parameters
        ----------------
        acdc: What signal to measure:
        direct current (1 or 'dc') or alternating current (2 or 'ac')

        rang: determine the RANGE option of the multimeter
        0 or 'auto' for AUTO option;
        a number that will set the current range, choose between the following(in ampers):
        100u, 1m, 10m, 100m, 1, 3 (if another number is entered, the nearest one from
        the previously listed will be taken as the current range).

        """
        if acdc == None:
            acdc = int(input("Press 1 for DC current or 2 for AC current: "))

        if (acdc == 1) or (acdc == 'dc'):
            if rang == None:
                autotest = float(self._dev.query('CURR:RANG:AUTO?'))
                rangetest = float(self._dev.query('CURR:RANG?'))
                if autotest == 1:
                    print("DC current range is set to: AUTO.\n")
                else:
                    print("DC current range is set to: ", rangetest, "A.\n")
            elif (rang == 'auto') or  (rang == 0):
                self._dev.write('CURR:RANG:AUTO ON')
                autotest = float(self._dev.query('CURR:RANG:AUTO?'))
                if autotest == 1:
                    print("DC current range is set to: AUTO.\n")
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('CURR:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('CURR:RANG?'))
                print("DC current range is set to: ", rangetest, "A.\n")
        elif (acdc == 2) or (acdc == 'ac'):
            if rang == None:
                autotest = float(self._dev.query('CURR:AC:RANG:AUTO?'))
                rangetest = float(self._dev.query('CURR:AC:RANG?'))
                if autotest == 1:
                    print("AC current range is set to: AUTO.\n")
                else:
                    print("AC current range is set to: ", rangetest, "A.\n")
            elif (rang == 'auto') or  (rang == 0):
                self._dev.write('CURR:AC:RANG:AUTO ON')
                autotest = float(self._dev.query('CURR:AC:RANG:AUTO?'))
                if autotest == 1:
                    print("AC current range is set to: AUTO.\n")
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('CURR:AC:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('CURR:AC:RANG?'))
                print("AC current range is set to: ", rangetest, "A.\n")
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def curr_int(self, typ = None, val = None):
        """Set or examine the current INTEGRATION option of the multimeter.

        Input parameters
        ----------------
        typ: determine the INTEGRATION option of the multimeter
        1 or 'NPLC' or 'nplc' for NPLC; 2 or 'APERTURE' or 'aperture' for APERTURE;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the voltage range).

        val = time parameter needed to set NPLC or APERTURE mode;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the time parameter).

        """
        if typ == None:
            atest = float(self._dev.query('CURR:APER:ENABLED?'))
            ntest = float(self._dev.query('CURR:NPLC?'))
            if atest == 1:
                atest2 = float(self._dev.query('CURR:APER?'))
                print("Current integration mode: APERTURE\nTime: ", atest2,"s.\n")
            else:
                print("Current integration mode: NPLC\nTime: ", ntest,"s.\n")
        elif (typ == 1) or (typ == 'NPLC') or (typ == 'nplc'):
            self._dev.write('CURR:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('CURR:NPLC?'))
            print("Current integration mode: NPLC\nTime: ", ntest,"s.\n")
        elif (typ == 2) or (typ == 'APERTURE') or (typ == 'aperture'):
            self._dev.write('CURR:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('CURR:APER?'))
            print("Current integration mode: APERTURE\nTime: ", atest2,"s.\n")
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def get_res(self):
        """Measures resistance.

        """
        r = float(self._dev.query('MEAS:RES?'))
        print("The resistance is: ", r, "ohms.\n")
        return r

    #===============================================================
    def res_range(self, rang = None):
        """Set or examine the resistance range.

        Input parameters
        ----------------
        rang: determine the RANGE option of the multimeter
        0 or 'auto' for AUTO option;
        a number that will set the resistance range, choose between the following (in ohms):
        100, 1k, 10k, 100k, 1M, 10M, 100M, 1G (if another number is entered, the nearest one from
        the previously listed will be taken as the current range).

        """
        if rang == None:
            autotest = float(self._dev.query('RES:RANG:AUTO?'))
            rangetest = float(self._dev.query('RES:RANG?'))
            if autotest == 1:
                print("Resistance range is set to: AUTO.\n")
            else:
                print("Resistance range is set to: ", rangetest, "ohms.\n")
        elif (rang == 'auto') or  (rang == 0):
            self._dev.write('RES:RANG:AUTO ON')
            autotest = float(self._dev.query('RES:RANG:AUTO?'))
            if autotest == 1:
                print("Resistance range is set to: AUTO.\n")
            else:
                raise ValueError("Error")
        else:
            self._dev.write('RES:RANG ', '%f' % float(rang))
            rangetest = float(self._dev.query('RES:RANG?'))
            print("Resistance range is set to: ", rangetest, "ohms.\n")

    #===============================================================
    def res_int(self, typ = None, val = None):
        """Set or examine the resistance INTEGRATION option of the multimeter.

        Input parameters
        ----------------
        typ: determine the INTEGRATION option of the multimeter
        1 or 'NPLC' or 'nplc' for NPLC; 2 or 'APERTURE' or 'aperture' for APERTURE;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the voltage range).

        val = time parameter needed to set NPLC or APERTURE mode;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the time parameter).

        """
        if typ == None:
            atest = float(self._dev.query('RES:APER:ENABLED?'))
            ntest = float(self._dev.query('RES:NPLC?'))
            if atest == 1:
                atest2 = float(self._dev.query('RES:APER?'))
                print("Resistance integration mode: APERTURE\nTime: ", atest2,"s.\n")
            else:
                print("Resistance integration mode: NPLC\nTime: ", ntest,"s.\n")
        elif (typ == 1) or (typ == 'NPLC') or (typ == 'nplc'):
            self._dev.write('RES:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('RES:NPLC?'))
            print("Resistance integration mode: NPLC\nTime: ", ntest,"s.\n")
        elif (typ == 2) or (typ == 'APERTURE') or (typ == 'aperture'):
            self._dev.write('RES:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('RES:APER?'))
            print("Resistance integration mode: APERTURE\nTime: ", atest2,"s.\n")
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def get_cap(self):
        """Measures capacitance.

        """
        c = float(self._dev.query('MEAS:CAP?'))
        print("The capacitance is: ", c, "F.\n")
        return c

    #===============================================================
    def cap_range(self, rang = None):
        """Set or examine the capacitance range.

        Input parameters
        ----------------
        rang: determine the RANGE option of the multimeter
        0 or 'auto' for AUTO option;
        a number that will set the capacitance range, choose between the following (in farads):
        1n, 10n, 100n, 1u, 10u (if another number is entered, the nearest one from
        the previously listed will be taken as the current range).

        """
        if rang == None:
            autotest = float(self._dev.query('CAP:RANG:AUTO?'))
            rangetest = float(self._dev.query('CAP:RANG?'))
            if autotest == 1:
                print("Capacitance range is set to: AUTO.\n")
            else:
                print("Capacitance range is set to: ", rangetest, "F.\n")
        elif (rang == 'auto') or  (rang == 0):
            self._dev.write('CAP:RANG:AUTO ON')
            autotest = float(self._dev.query('CAP:RANG:AUTO?'))
            if autotest == 1:
                print("Capacitance range is set to: AUTO.\n")
            else:
                raise ValueError("Error")
        else:
            self._dev.write('CAP:RANG ', '%f' % float(rang))
            rangetest = float(self._dev.query('CAP:RANG?'))
            print("Capacitance range is set to: ", rangetest, "F.\n")

    #===============================================================
    def inputz(self, imp = None):
        """Set or examine the INPUT Z voltage option of the multimeter.

        Input parameters
        ----------------
        imp: selects the wanted INPUT Z option:
        0 or '10M' for 10M; 1 or 'Hi-Z' for Hi-Z; no input to only examine
        the current INPUT Z status.

        """
        if imp == None:
            a = float(self._dev.query('VOLT:IMP:AUTO?'))
        elif (imp == 0) or (imp == '10M'):
            self._dev.write('VOLT:IMP:AUTO OFF')
            a = float(self._dev.query('VOLT:IMP:AUTO?'))
        elif (imp == 1) or (imp == 'Hi-Z'):
            self._dev.write('VOLT:IMP:AUTO ON')
            a = float(self._dev.query('VOLT:IMP:AUTO?'))
        else:
            raise ValueError("Incorrect input.\n")

        if a == 0:
            print("The input impedance is: 10Mohm.\n")
            output = '10M'
        elif a == 1:
            print("The input impedance status is: Hi-Z.\n")
            output = 'Hi-Z'
        else:
            raise ValueError("Error")
        return output

    #===============================================================
    def remove_error(self):
        """Remove a single error.

        """
        self._dev.query('SYS:ERR?')

    #===============================================================
    def remove_errors(self):
        """Remove all errors.

        """
        self._dev.write('*CLS')

    #===============================================================
    # PRIVATE METHODS
    #===============================================================
    def _name(self):
        """Return device name.

        """
        name = self._dev.query('*IDN?')
        name = name.rstrip('\n')
        return name
    #===============================================================
    def _reset(self):
        """Reset device.

        """
        self._dev.write('*RST')
        time.sleep(1)

    #===============================================================
    def _write_sent(self, sentence):
        """Write a sentence in a file.

        Input parameters
        ----------------
        sentence: predetermined

        """
        with open(self.fname, "a") as f:
            f.write(sentence)

    #===============================================================
    def _timestamp(self):
        """Creates a timestamp both in float and string format.


        """
        t0 = time.asctime(time.localtime(time.time()))
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
        for i in range(2):
            t3.remove(' ')
        for i in [2, 5, 14]:
            t3.insert(i, '_')
        day = t3[3:6]
        month = t3[0:3]
        year = t3[15:19]
        handm = t3[5:11]
        t4 = day + month + year + handm
        timestr=''.join(t4)
        self.time = timestr
