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
    def __init__(self, addr, fname = None):
        """Initialization.

        """
        rm = visa.ResourceManager()
        self._dev = rm.open_resource('GPIB0::' + str(addr) + '::INSTR')

        # get instrument address

        self.addr = addr
        self.fname = fname

        # get instrument name
        self.name = self._name()

        self._timestamp()

        self._sent = str(self.name) + "\nTime: " + str(self.time) + "\nAddress: " + str(self.addr) + "\n"

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

        if acdc in [1, '1', 'dc']:
            u = float(self._dev.query('MEAS?'))
        elif acdc in [2, '2', 'ac']:
            u = float(self._dev.query('MEAS:AC?'))
        else:
            raise ValueError("Error")
        self._timestamp()
        sentence = self._sent + "The voltage is: " + str(u) + "V.\n\n"
        print(sentence)
        self._write_sent(sentence)
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

        if acdc in [1, '1', 'dc']:
            if rang == None:
                autotest = float(self._dev.query('VOLT:RANG:AUTO?'))
                rangetest = float(self._dev.query('VOLT:RANG?'))
                self._timestamp()
                if autotest == 1:
                    sentence = self._sent + "DC voltage range is set to: AUTO.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
                else:
                    sentence = self._sent + "DC voltage range is set to: " + str(rangetest) + "V.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
            elif rang in [0, '0', 'auto']:
                self._dev.write('VOLT:RANG:AUTO ON')
                autotest = float(self._dev.query('VOLT:RANG:AUTO?'))
                if autotest == 1:
                    self._timestamp()
                    sentence = self._sent + "DC voltage range is set to: AUTO.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('VOLT:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('VOLT:RANG?'))
                self._timestamp()
                sentence = self._sent + "DC voltage range is set to: " + str(rangetest) + "V.\n\n"
                print(sentence)
                self._write_sent(sentence)
        elif acdc in [2, '2', 'ac']:
            if rang == None:
                autotest = float(self._dev.query('VOLT:AC:RANG:AUTO?'))
                rangetest = float(self._dev.query('VOLT:AC:RANG?'))
                self._timestamp()
                if autotest == 1:
                    sentence = self._sent + "AC voltage range is set to: AUTO.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
                else:
                    sentence = self._sent + "AC voltage range is set to: " + str(rangetest) + "V.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
            elif rang in [0, '0', 'auto']:
                self._dev.write('VOLT:AC:RANG:AUTO ON')
                autotest = float(self._dev.query('VOLT:AC:RANG:AUTO?'))
                if autotest == 1:
                    self._timestamp()
                    sentence = self._sent + "AC voltage range is set to: AUTO.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('VOLT:AC:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('VOLT:AC:RANG?'))
                self._timestamp()
                sentence = self._sent + "AC voltage range is set to: " + str(rangetest) + "V.\n\n"
                print(sentence)
                self._write_sent(sentence)
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
            self._timestamp()
            if atest == 1:
                atest2 = float(self._dev.query('VOLT:APER?'))
                sentence = self._sent + "Voltage integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
                print(sentence)
                self._write_sent(sentence)
            else:
                sentence = self._sent + "Voltage integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
                print(sentence)
                self._write_sent(sentence)
        elif typ in [1, '1', 'NPLC', 'nplc']:
            self._dev.write('VOLT:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('VOLT:NPLC?'))
            self._timestamp()
            sentence = self._sent + "Voltage integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
            print(sentence)
            self._write_sent(sentence)
        elif typ in [2, '2', 'APERTURE', 'aperture']:
            self._dev.write('VOLT:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('VOLT:APER?'))
            self._timestamp()
            sentence = self._sent + "Voltage integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
            print(sentence)
            self._write_sent(sentence)
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

        if acdc in [1, '1', 'dc']:
            i = float(self._dev.query('MEAS:CURR?'))
        elif acdc in [2, '2', 'ac']:
            i = float(self._dev.query('MEAS:CURR:AC?'))
        else:
            raise ValueError("Error")
        self._timestamp()
        sentence = self._sent + "The current is: " + str(i) + "A.\n\n"
        print(sentence)
        self._write_sent(sentence)
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

        if acdc in [1, '1', 'dc']:
            if rang == None:
                autotest = float(self._dev.query('CURR:RANG:AUTO?'))
                rangetest = float(self._dev.query('CURR:RANG?'))
                self._timestamp()
                if autotest == 1:
                    sentence = self._sent + "DC current range is set to: AUTO.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
                else:
                    sentence = self._sent + "DC current range is set to: " + str(rangetest) + "A.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
            elif rang in [0, '0', 'auto']:
                self._dev.write('CURR:RANG:AUTO ON')
                autotest = float(self._dev.query('CURR:RANG:AUTO?'))
                if autotest == 1:
                    self._timestamp()
                    sentence = self._sent + "DC current range is set to: AUTO.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('CURR:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('CURR:RANG?'))
                self._timestamp()
                sentence = self._sent + "DC current range is set to: " + str(rangetest) + "A.\n\n"
                print(sentence)
                self._write_sent(sentence)
        elif acdc in [2, '2', 'ac']:
            if rang == None:
                autotest = float(self._dev.query('CURR:AC:RANG:AUTO?'))
                rangetest = float(self._dev.query('CURR:AC:RANG?'))
                self._timestamp()
                if autotest == 1:
                    sentence = self._sent + "AC current range is set to: AUTO.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
                else:
                    sentence = self._sent + "AC current range is set to: " + str(rangetest) + "A.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
            elif rang in [0, '0', 'auto']:
                self._dev.write('CURR:AC:RANG:AUTO ON')
                autotest = float(self._dev.query('CURR:AC:RANG:AUTO?'))
                if autotest == 1:
                    self._timestamp()
                    sentence = self._sent + "AC current range is set to: AUTO.\n\n"
                    print(sentence)
                    self._write_sent(sentence)
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('CURR:AC:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('CURR:AC:RANG?'))
                self._timestamp()
                sentence = self._sent + "AC current range is set to: " + str(rangetest) + "A.\n\n"
                print(sentence)
                self._write_sent(sentence)
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
                self._timestamp()
                sentence = self._sent + "Current integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
                print(sentence)
                self._write_sent(sentence)
            else:
                self._timestamp()
                sentence = self._sent + "Current integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
                print(sentence)
                self._write_sent(sentence)
        elif typ in [1, '1', 'NPLC', 'nplc']:
            self._dev.write('CURR:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('CURR:NPLC?'))
            self._timestamp()
            sentence = self._sent + "Current integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
            print(sentence)
            self._write_sent(sentence)
        elif typ in [2, '2', 'APERTURE', 'aperture']:
            self._dev.write('CURR:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('CURR:APER?'))
            self._timestamp()
            sentence = self._sent + "Current integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
            print(sentence)
            self._write_sent(sentence)
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def get_res(self):
        """Measures resistance.

        """
        r = float(self._dev.query('MEAS:RES?'))
        self._timestamp()
        sentence = self._sent + "The resistance is: " + str(r) + "ohms.\n\n"
        print(sentence)
        self._write_sent(sentence)
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
            self._timestamp()
            if autotest == 1:
                sentence = self._sent + "Resistance range is set to: AUTO.\n\n"
                print(sentence)
                self._write_sent(sentence)
            else:
                sentence = self._sent + "Resistance range is set to: " + str(rangetest) + "ohms.\n\n"
                print(sentence)
                self._write_sent(sentence)
        elif rang in [0, '0', 'auto']:
            self._dev.write('RES:RANG:AUTO ON')
            autotest = float(self._dev.query('RES:RANG:AUTO?'))
            if autotest == 1:
                self._timestamp()
                sentence = self._sent + "Resistance range is set to: AUTO.\n\n"
                print(sentence)
                self._write_sent(sentence)
            else:
                raise ValueError("Error")
        else:
            self._dev.write('RES:RANG ', '%f' % float(rang))
            rangetest = float(self._dev.query('RES:RANG?'))
            self._timestamp()
            sentence = self._sent + "Resistance range is set to: " + str(rangetest) + "ohms.\n\n"
            print(sentence)
            self._write_sent(sentence)

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
                self._timestamp()
                sentence = self._sent + "Resistance integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
                print(sentence)
                self._write_sent(sentence)
            else:
                self._timestamp()
                sentence = self._sent + "Resistance integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
                print(sentence)
                self._write_sent(sentence)
        elif typ in [1, '1', 'NPLC', 'nplc']:
            self._dev.write('RES:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('RES:NPLC?'))
            self._timestamp()
            sentence = self._sent + "Resistance integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
            print(sentence)
            self._write_sent(sentence)
        elif typ in [2, '2', 'APERTURE', 'aperture']:
            self._dev.write('RES:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('RES:APER?'))
            self._timestamp()
            sentence = self._sent + "Resistance integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
            print(sentence)
            self._write_sent(sentence)
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def get_cap(self):
        """Measures capacitance.

        """
        c = float(self._dev.query('MEAS:CAP?'))
        self._timestamp()
        sentence = self._sent + "The capacitance is: " + str(c) + "F.\n\n"
        print(sentence)
        self._write_sent(sentence)
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
            self._timestamp()
            if autotest == 1:
                sentence = self._sent + "Capacitance range is set to: AUTO.\n\n"
                print(sentence)
                self._write_sent(sentence)
            else:
                sentence = self._sent + "Capacitance range is set to: " + str(rangetest) + "F.\n\n"
                print(sentence)
                self._write_sent(sentence)
        elif rang in [0, '0', 'auto']:
            self._dev.write('CAP:RANG:AUTO ON')
            autotest = float(self._dev.query('CAP:RANG:AUTO?'))
            self._timestamp()
            if autotest == 1:
                sentence = self._sent + "Capacitance range is set to: AUTO.\n\n"
                print(sentence)
                self._write_sent(sentence)
            else:
                raise ValueError("Error")
        else:
            self._dev.write('CAP:RANG ', '%f' % float(rang))
            rangetest = float(self._dev.query('CAP:RANG?'))
            self._timestamp()
            sentence = self._sent + "Capacitance range is set to: " + str(rangetest) + "F.\n\n"
            print(sentence)
            self._write_sent(sentence)

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
        elif imp in [0, '0', '10M']:
            self._dev.write('VOLT:IMP:AUTO OFF')
            a = float(self._dev.query('VOLT:IMP:AUTO?'))
        elif imp in [1, '1', 'Hi-Z']:
            self._dev.write('VOLT:IMP:AUTO ON')
            a = float(self._dev.query('VOLT:IMP:AUTO?'))
        else:
            raise ValueError("Incorrect input.\n")

        self._timestamp()

        if a == 0:
            sentence = self._sent + "The input impedance is: 10Mohm.\n\n"
            print(sentence)
            self._write_sent(sentence)
            output = '10M'
        elif a == 1:
            sentence = self._sent + "The input impedance status is: Hi-Z.\n\n"
            print(sentence)
            self._write_sent(sentence)
            output = 'Hi-Z'
        else:
            raise ValueError("Error")
        return output
