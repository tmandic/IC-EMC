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

        self._sent1 = str(self.name) + "\nTime: "
        self._sent2 = "\nAddress: " + str(self.addr) + "\n"

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
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + "The voltage is: " + str(u) + "V.\n\n"
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
        return u

    #===============================================================
    def volt_range(self, acdc = None, rang = None):
        """Set or examine the voltage range.

        Input parameters
        ----------------
        acdc: What signal to measure:
        direct current (1 or 'dc') or alternating current (2 or 'ac')

        rang: determine the RANGE option of the multimeter (if nothing or 'None' is entered, the function will only examine the parameter)
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
                self._sent = self._sent1 + str(self.time) + self._sent2
                if autotest == 1:
                    sentence = self._sent + "DC voltage range is set to: AUTO.\n\n"
                    print(sentence)
                    if self.fname != None:
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
                    self._sent = self._sent1 + str(self.time) + self._sent2
                    sentence = self._sent + "DC voltage range is set to: AUTO.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('VOLT:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('VOLT:RANG?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "DC voltage range is set to: " + str(rangetest) + "V.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
        elif acdc in [2, '2', 'ac']:
            if rang == None:
                autotest = float(self._dev.query('VOLT:AC:RANG:AUTO?'))
                rangetest = float(self._dev.query('VOLT:AC:RANG?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                if autotest == 1:
                    sentence = self._sent + "AC voltage range is set to: AUTO.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
                else:
                    sentence = self._sent + "AC voltage range is set to: " + str(rangetest) + "V.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
            elif rang in [0, '0', 'auto']:
                self._dev.write('VOLT:AC:RANG:AUTO ON')
                autotest = float(self._dev.query('VOLT:AC:RANG:AUTO?'))
                if autotest == 1:
                    self._timestamp()
                    self._sent = self._sent1 + str(self.time) + self._sent2
                    sentence = self._sent + "AC voltage range is set to: AUTO.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('VOLT:AC:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('VOLT:AC:RANG?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "AC voltage range is set to: " + str(rangetest) + "V.\n\n"
                print(sentence)
                if self.fname != None:
                        self._write_sent(sentence)
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def volt_int(self, typ = None, val = None):
        """Set or examine the voltage INTEGRATION option of the multimeter.

        Input parameters
        ----------------
        typ: determine the INTEGRATION option of the multimeter (if nothing or 'None' is entered, the function will only examine the parameter)
        1 or 'NPLC' or 'nplc' for NPLC; 2 or 'APERTURE' or 'aperture' for APERTURE;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the voltage range).

        val = time parameter needed to set NPLC or APERTURE mode;
        in case of NPLC choose between the following(in seconds)
        (if nothing or 'None' is entered, the function will only examine the parameter)
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the time parameter).

        """
        if typ == None:
            atest = float(self._dev.query('VOLT:APER:ENABLED?'))
            ntest = float(self._dev.query('VOLT:NPLC?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            if atest == 1:
                atest2 = float(self._dev.query('VOLT:APER?'))
                sentence = self._sent + "Voltage integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
            else:
                sentence = self._sent + "Voltage integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
        elif typ in [1, '1', 'NPLC', 'nplc']:
            if val == None:
                val = float(input("Enter the wanted time parameter for integration mode: "))
            self._dev.write('VOLT:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('VOLT:NPLC?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Voltage integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
        elif typ in [2, '2', 'APERTURE', 'aperture']:
            if val == None:
                val = float(input("Enter the wanted time parameter for integration mode: "))
            self._dev.write('VOLT:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('VOLT:APER?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Voltage integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
            print(sentence)
            if self.fname != None:
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
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + "The current is: " + str(i) + "A.\n\n"
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
        return i

    #===============================================================
    def curr_range(self, acdc = None, rang = None):
        """Set or examine the current range.

        Input parameters
        ----------------
        acdc: What signal to measure:
        direct current (1 or 'dc') or alternating current (2 or 'ac')

        rang: determine the RANGE option of the multimeter (if nothing or 'None' is entered, the function will only examine the parameter)
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
                self._sent = self._sent1 + str(self.time) + self._sent2
                if autotest == 1:
                    sentence = self._sent + "DC current range is set to: AUTO.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
                else:
                    sentence = self._sent + "DC current range is set to: " + str(rangetest) + "A.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
            elif rang in [0, '0', 'auto']:
                self._dev.write('CURR:RANG:AUTO ON')
                autotest = float(self._dev.query('CURR:RANG:AUTO?'))
                if autotest == 1:
                    self._timestamp()
                    self._sent = self._sent1 + str(self.time) + self._sent2
                    sentence = self._sent + "DC current range is set to: AUTO.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('CURR:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('CURR:RANG?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "DC current range is set to: " + str(rangetest) + "A.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
        elif acdc in [2, '2', 'ac']:
            if rang == None:
                autotest = float(self._dev.query('CURR:AC:RANG:AUTO?'))
                rangetest = float(self._dev.query('CURR:AC:RANG?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                if autotest == 1:
                    sentence = self._sent + "AC current range is set to: AUTO.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
                else:
                    sentence = self._sent + "AC current range is set to: " + str(rangetest) + "A.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
            elif rang in [0, '0', 'auto']:
                self._dev.write('CURR:AC:RANG:AUTO ON')
                autotest = float(self._dev.query('CURR:AC:RANG:AUTO?'))
                if autotest == 1:
                    self._timestamp()
                    self._sent = self._sent1 + str(self.time) + self._sent2
                    sentence = self._sent + "AC current range is set to: AUTO.\n\n"
                    print(sentence)
                    if self.fname != None:
                        self._write_sent(sentence)
                else:
                    raise ValueError("Error")
            else:
                self._dev.write('CURR:AC:RANG ', '%f' % float(rang))
                rangetest = float(self._dev.query('CURR:AC:RANG?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "AC current range is set to: " + str(rangetest) + "A.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def curr_int(self, typ = None, val = None):
        """Set or examine the current INTEGRATION option of the multimeter.

        Input parameters
        ----------------
        typ: determine the INTEGRATION option of the multimeter (if nothing or 'None' is entered, the function will only examine the parameter)
        1 or 'NPLC' or 'nplc' for NPLC; 2 or 'APERTURE' or 'aperture' for APERTURE;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the voltage range).

        val = time parameter needed to set NPLC or APERTURE mode;
        in case of NPLC choose between the following(in seconds)
        (if nothing or 'None' is entered, the function will only examine the parameter)
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the time parameter).

        """
        if typ == None:
            atest = float(self._dev.query('CURR:APER:ENABLED?'))
            ntest = float(self._dev.query('CURR:NPLC?'))
            if atest == 1:
                atest2 = float(self._dev.query('CURR:APER?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "Current integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
            else:
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "Current integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
        elif typ in [1, '1', 'NPLC', 'nplc']:
            if val == None:
                val = float(input("Enter the wanted time parameter for integration mode: "))
            self._dev.write('CURR:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('CURR:NPLC?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Current integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
        elif typ in [2, '2', 'APERTURE', 'aperture']:
            if val == None:
                val = float(input("Enter the wanted time parameter for integration mode: "))
            self._dev.write('CURR:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('CURR:APER?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Current integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def get_res(self):
        """Measures resistance.

        """
        r = float(self._dev.query('MEAS:RES?'))
        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + "The resistance is: " + str(r) + "ohms.\n\n"
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
        return r

    #===============================================================
    def res_range(self, rang = None):
        """Set or examine the resistance range.

        Input parameters
        ----------------
        rang: determine the RANGE option of the multimeter (if nothing or 'None' is entered, the function will only examine the parameter)
        0 or 'auto' for AUTO option;
        a number that will set the resistance range, choose between the following (in ohms):
        100, 1k, 10k, 100k, 1M, 10M, 100M, 1G (if another number is entered, the nearest one from
        the previously listed will be taken as the current range).

        """
        if rang == None:
            autotest = float(self._dev.query('RES:RANG:AUTO?'))
            rangetest = float(self._dev.query('RES:RANG?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            if autotest == 1:
                sentence = self._sent + "Resistance range is set to: AUTO.\n\n"
                print(sentence)
                if self.fname != None:
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
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "Resistance range is set to: AUTO.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
            else:
                raise ValueError("Error")
        else:
            self._dev.write('RES:RANG ', '%f' % float(rang))
            rangetest = float(self._dev.query('RES:RANG?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Resistance range is set to: " + str(rangetest) + "ohms.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)

    #===============================================================
    def res_int(self, typ = None, val = None):
        """Set or examine the resistance INTEGRATION option of the multimeter.

        Input parameters
        ----------------
        typ: determine the INTEGRATION option of the multimeter (if nothing or 'None' is entered, the function will only examine the parameter)
        1 or 'NPLC' or 'nplc' for NPLC; 2 or 'APERTURE' or 'aperture' for APERTURE;
        in case of NPLC choose between the following(in seconds):
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the voltage range).

        val = time parameter needed to set NPLC or APERTURE mode;
        in case of NPLC choose between the following(in seconds)
        (if nothing or 'None' is entered, the function will only examine the parameter)
        0.006, 0.02, 0.06, 0.2, 1, 2, 10, 100 (if another number is entered, the nearest one from
        the previously listed will be taken as the time parameter).

        """
        if typ == None:
            atest = float(self._dev.query('RES:APER:ENABLED?'))
            ntest = float(self._dev.query('RES:NPLC?'))
            if atest == 1:
                atest2 = float(self._dev.query('RES:APER?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "Resistance integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
            else:
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "Resistance integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
        elif typ in [1, '1', 'NPLC', 'nplc']:
            if val == None:
                val = float(input("Enter the wanted time parameter for integration mode: "))
            self._dev.write('RES:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('RES:NPLC?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Resistance integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
        elif typ in [2, '2', 'APERTURE', 'aperture']:
            if val == None:
                val = float(input("Enter the wanted time parameter for integration mode: "))
            self._dev.write('RES:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('RES:APER?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Resistance integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
        else:
            raise ValueError("Incorrect input.\n")

    #===============================================================
    def get_cap(self):
        """Measures capacitance.

        """
        c = float(self._dev.query('MEAS:CAP?'))
        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + "The capacitance is: " + str(c) + "F.\n\n"
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
        return c

    #===============================================================
    def cap_range(self, rang = None):
        """Set or examine the capacitance range.

        Input parameters
        ----------------
        rang: determine the RANGE option of the multimeter (if nothing or 'None' is entered, the function will only examine the parameter)
        0 or 'auto' for AUTO option;
        a number that will set the capacitance range, choose between the following (in farads):
        1n, 10n, 100n, 1u, 10u (if another number is entered, the nearest one from
        the previously listed will be taken as the current range).

        """
        if rang == None:
            autotest = float(self._dev.query('CAP:RANG:AUTO?'))
            rangetest = float(self._dev.query('CAP:RANG?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            if autotest == 1:
                sentence = self._sent + "Capacitance range is set to: AUTO.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
            else:
                sentence = self._sent + "Capacitance range is set to: " + str(rangetest) + "F.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
        elif rang in [0, '0', 'auto']:
            self._dev.write('CAP:RANG:AUTO ON')
            autotest = float(self._dev.query('CAP:RANG:AUTO?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            if autotest == 1:
                sentence = self._sent + "Capacitance range is set to: AUTO.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
            else:
                raise ValueError("Error")
        else:
            self._dev.write('CAP:RANG ', '%f' % float(rang))
            rangetest = float(self._dev.query('CAP:RANG?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Capacitance range is set to: " + str(rangetest) + "F.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)

    #===============================================================
    def get_temp(self):
        """Measures temperature.

        Returns temperature.

        """
        t = float(self._dev.query('MEAS:TEMP?'))
        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent0 = " {}.\n\n".format(self.unit_string)
        sentence = self._sent + "The temperature is: " + str(t) + sent0
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
        return t

    #===============================================================
    def temp_null(self, null = None, nullval = None):
        """Set or examine temperature measurement null value.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        null - sets the null measurement feature to ON or OFF
        ON - 1, '1', 'on', 'ON'
        OFF - 2, '2', 'off', 'OFF'

        nullval - edits the null value (if null is set to ON)

        """

    #===============================================================
    def set_temp_meas(self, typ = None, wire = None):
        """Set or examine temperature measurement probe type.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        typ - sets the probe type to RTD or THERMISTOR.
        RTD - 1, '1', 'r', 'R', 'rtd', 'RTD'
        THERMISTOR - 2, '2', 't', 'T', 'therm', 'THERM', 'thermistor', 'THERMISTOR'

        wire - sets up a 2-wire or 4-wire measurement
        2-wire - 2, '2', '2w', '2W'
        4-wire - 4, '4', '4w', '4W'

        """
        if (typ == None) and (wire == None):
            pass
        elif typ in [1, '1', 'r', 'R', 'rtd', 'RTD'] and wire in [2, '2', '2w', '2W']:
            self.probetype = 'RTD'
            probetypea = 'RTD'
        elif typ in [1, '1', 'r', 'R', 'rtd', 'RTD'] and wire in [4, '4', '4w', '4W']:
            self.probetype = 'FRTD'
            probetypea = 'FRTD'
        elif typ in [2, '2', 't', 'T', 'therm', 'THERM', 'thermistor', 'THERMISTOR'] and wire in [2, '2', '2w', '2W']:
            self.probetype = 'THERMISTOR'
            probetypea = 'THERMISTOR'
        elif typ in [2, '2', 't', 'T', 'therm', 'THERM', 'thermistor', 'THERMISTOR'] and wire in [4, '4', '4w', '4W']:
            self.probetype = 'FTHERMISTOR'
            probetypea = 'DEF'
        else:
            raise ValueError("Incorrect input.\n")

        if (typ != None) and (wire != None):
            self._dev.write("CONF:TEMP {}".format(probetypea))

        probetest = self._dev.query("CONF?")
        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The measurement is set up as {}".format(probetest)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

    #===============================================================
    def temp_offset_comp(self, offset = None):
        """Set or examine the offset compensation feature for RTD probes.

        Input parameters
        ----------------
        offset - turn the offset compensation feature ON or OFF (if nothing or 'None' is entered, the function will only examine the parameter)
        ON - 1, '1', 'on', 'ON'
        OFF - 2, '2', 'off', 'OFF'

        """
        if self.probetype in ['RTD', 'FRTD']:
            if offset == None:
                pass
            elif offset in [1, '1', 'on', 'ON']:
                offset = 'ON'
                self._dev.write("TEMP:TRAN:{}:OCOM {}".format(self.probetype, offset))
            elif offset in [2, '2', 'off', 'OFF']:
                offset = 'OFF'
                self._dev.write("TEMP:TRAN:{}:OCOM {}".format(self.probetype, offset))

            else:
                raise ValueError("Incorrect input.\n")

            offset = self._dev.query("TEMP:TRAN:{}:OCOM?".format(self.probetype))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sent = "Offset is set up as {}.\n".format(offset)
            sentence = self._sent + sent
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)

        elif self.probetype in ['THERMISTOR', 'FTHERMISTOR']:
            sent = "Offset compensation feature can only be set up for RTD probes.\n"
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + sent
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)

        else:
            sent = "To turn the offset compensation feature ON or OFF, you have to set up the measurement type to RTD.\n"
            sent = "Offset compensation feature can only be set up for RTD probes.\n"
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + sent
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)

    #===============================================================
    def temp_unit(self, unit = None):
        """Setor examine the temperature unit.

        Returns temperature unit.


        Input parameters
        ----------------
        unit - temperature unit (if nothing or 'None' is entered, the function will only examine the parameter)
        C - 1, '1', 'C', '°C'
        F - 2, '2', 'F', '°F'
        K - 3, '3', 'K'

        """
        if unit == None:
            unit0 = None
        elif unit in [1, '1', 'C', '°C']:
            unit0 = 'C'
        elif unit in [2, '2', 'F', '°F']:
            unit0 = 'F'
        elif unit in [3, '3', 'K']:
            unit0 = 'K'
        else:
            raise ValueError("Incorrect input.\n")

        if unit != None:
            self._dev.write('UNIT:TEMP {}'.format(unit0))

        self.unit = self._dev.query('UNIT:TEMP?')

        if self.unit != unit0:
            raise ValueError("Error during temperature unit test.\n")

        if self.unit == 'K':
            self.unit_string = 'K'
        elif self.unit in ['C', 'F']
            self.unit_string = '°' + self.unit
        else:
            raise ValueError("Error during temperature unit test string setup.\n")

        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + "The temperature unit is: " + self._unit_string
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
        return self.unit

    #===============================================================
    def temp_int(self, typ = None, val = None):
        """Set or examine the temperature INTEGRATION option of the multimeter.

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
            atest = float(self._dev.query('TEMP:APER:ENABLED?'))
            ntest = float(self._dev.query('TEMP:NPLC?'))
            if atest == 1:
                atest2 = float(self._dev.query('TEMP:APER?'))
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "Temperature integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
            else:
                self._timestamp()
                self._sent = self._sent1 + str(self.time) + self._sent2
                sentence = self._sent + "Temperature integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
                print(sentence)
                if self.fname != None:
                    self._write_sent(sentence)
        elif typ in [1, '1', 'NPLC', 'nplc']:
            if val == None:
                val = float(input("Enter the wanted time parameter for integration mode: "))
            self._dev.write('TEMP:NPLC ', '%f' % float(val))
            ntest = float(self._dev.query('TEMP:NPLC?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Temperature integration mode: NPLC\nTime: " + str(ntest) + "s.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
        elif typ in [2, '2', 'APERTURE', 'aperture']:
            if val == None:
                val = float(input("Enter the wanted time parameter for integration mode: "))
            self._dev.write('TEMP:APER ', '%f' % float(val))
            atest2 = float(self._dev.query('TEMP:APER?'))
            self._timestamp()
            self._sent = self._sent1 + str(self.time) + self._sent2
            sentence = self._sent + "Temperature integration mode: APERTURE\nTime: " + str(atest2) + "s.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
        else:
            raise ValueError("Incorrect input.\n")

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
        self._sent = self._sent1 + str(self.time) + self._sent2

        if a == 0:
            sentence = self._sent + "The input impedance is: 10Mohm.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
            output = '10M'
        elif a == 1:
            sentence = self._sent + "The input impedance status is: Hi-Z.\n\n"
            print(sentence)
            if self.fname != None:
                self._write_sent(sentence)
            output = 'Hi-Z'
        else:
            raise ValueError("Error")
        return output
