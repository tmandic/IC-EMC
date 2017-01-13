# -*- coding: utf-8 -*-
import time
import visa
import numpy as np
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class AgilentU2722A(GPIB):
    """USB Modular Source Measure Units Agilent U2732A.

    """
    #===============================================================
    def __init__(self, addr, chan = None, fname = None):
        """Initialization.

        """
        rm = visa.ResourceManager()
        self._dev = rm.open_resource('USB0::' + str(addr) + '::INSTR')

        # get instrument address

        self.addr = addr
        self.fname = fname

        # get instrument name
        self.name = self._name()

        self._timestamp()

        self._sel_chan(chan = chan)

        self.volt_range()
        self.volt_limit()
        self.curr_range()
        self.curr_limit()
        self.sweep_points(100)
        self.tinterval(1)
        self.volt_outval = None
        self.curr_outval = None

    #===============================================================
    def meas(self, typ = None, dataoutput = 'array'):
        """Measure the output voltage or current on the set.

        Returns measurement value in V/A.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will measure the current in case of a voltage source, or voltage in case of a current source)
        typ: selects voltage or current measurement (strings may be entered in uppercase)
        voltage - 1, '1', 'v', 'volt', 'voltage'
        curr - 2, '2', 'i', 'curr', 'current'

        dataoutput: scalar or array measurement (strings may be entered in uppercase)
        (default value is set to scalar)
        scalar - 1, '1', 's', 'scal', 'scalar'
        array - 2, '2', 'a', 'arr', 'array'
        """
        if typ == None:
            if (self.volt_outval == None) and (self.curr_outval == None):
                raise ValueError("The source on channel {} hasn't been set up yet.\n".format(self.chan))
            elif self.volt_outval == None:
                typ = 'VOLT'
                typ_sent = 'voltage'
                unit = 'V'
            elif self.curr_outval == None:
                typ = 'CURR'
                typ_sent = 'current'
                unit = 'A'
            else:
                raise ValueError('Error.\n')
        elif (typ == 1) or (str(typ).lower() in ['1', 'v', 'volt', 'voltage']):
            typ = 'VOLT'
            typ_sent = 'voltage'
            unit = 'V'
        elif (typ == 2) or (str(typ).lower() in ['2', 'i', 'curr', 'current']):
            typ = 'CURR'
            typ_sent = 'current'
            unit = 'A'
        else:
            raise ValueError("Wrong input.\n")

        if (dataoutput == 1) or (dataoutput in ['1', 's', 'scal', 'scalar']):
            measval = float(str(self._dev.query("MEAS:{}? (@{})".format(typ, self.chan))).rstrip('\n'))
            sent = "The measured {} is {} {}.\n".format(typ_sent, measval, unit)
        elif (dataoutput == 2) or (dataoutput in [2, '2', 'a', 'arr', 'array']):
            measval1 = self._dev.query("MEAS:ARR:{}? (@{})".format(typ, self.chan))
            measval2 = [float(s) for s in measval1.split(" ,")]
            measval = sum(np.asarray(measval2))/len(measval2)
            sent = "Number of points measured: {}.\nThe average measured {} is {} {}.\n".format(len(measval2),typ_sent, measval, unit)
        else:
            raise ValueError("Wrong input.\n")

        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return measval

    #===============================================================
    def meas_temp(self):
        """Measure the temperature.

        Returns measurement value in °C.
        """
        temp = float(str(self._dev.query('MEAS:TEMP?'.format(self.chan))).rstrip('\n'))
        sent = "The measured temperature is {} °C.\n".format(temp)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return temp

    #===============================================================
    def volt_out(self, outval = None):
        """Set or examine the output voltage.

        Returns voltage output value in V.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        outval: output voltage [V] (must not exceed the set voltage range)
        """
        if outval == None:
            pass
        else:
            if float(outval)>self.volt_rangval_float:
                print("The entered output value exceeds the set voltage range, which is: {}\n".format(self.volt_rangval))
            else:
                self._dev.write('VOLT {}, (@{})'.format(float(outval), self.chan))

        self.volt_outval = float(str(self._dev.query('VOLT? (@{})'.format(self.chan))).rstrip('\n'))
        self.curr_outval = None
        sent = "The output voltage is set to: {} V.\n".format(self.volt_outval)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.volt_outval

    #===============================================================
    def volt_range(self, rang = None):
        """Set or examine the voltage range.

        Returns voltage range.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        range: voltage range (strings can be entered in uppercase)
        R2V - 0, '0', 2, '2', '2v', '2 v', 'r2v'
        R20V - 1, '1', 20, '20', '20v', '20 v', 'r20v'
        """
        if rang == None:
            pass
        elif (rang in [0, 2]) or (str(rang).lower() in ['0', '2', '2v', '2 v', 'r2v']):
            self._dev.write("VOLT:RANG R2V, (@{})".format(self.chan))
        elif (rang in [1, 20]) or (str(rang).lower() in ['1', '20', '20v', '20 v', 'r20v']):
            self._dev.write("VOLT:RANG R20V, (@{})".format(self.chan))

        self.volt_rangval = str(self._dev.query("VOLT:RANG? (@{})".format(self.chan))).rstrip('\n')
        self.volt_rangval_float = float(self.volt_rangval.lstrip('R').rstrip('V'))

        sent = "The voltage range is set to: {}.\n".format(self.volt_rangval)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.volt_rangval_float

    #===============================================================
    def volt_limit(self, limit = None):
        """Set or examine the voltage limit.

        Returns voltage limit in V.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        limit: voltage limit [V] (must not exceed the set voltage range)
        """
        if limit == None:
            pass
        else:
            if float(limit)>self.volt_rangval_float:
                print("The entered voltage limit exceeds the set voltage range, which is: {}\n".format(self.volt_rangval))
            else:
                self._dev.write("VOLT:LIM {}, (@{})".format(float(limit),self.chan))

        self.volt_limitval = float(str(self._dev.query("VOLT:LIM? (@{})".format(self.chan))).rstrip('\n'))

        sent = "The voltage limit is set to: {} V.\n".format(self.volt_limitval)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.volt_limitval

    #===============================================================
    def volt_trig(self, trig = None):
        """Set or examine the voltage trigger.

        Returns voltage trigger.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        trig: voltage trigger [V]
        """
        if trig == None:
            pass
        else:
            self._dev.write("VOLT:TRIG {}, (@{})".format(float(trig), self.chan))

        self.volt_trigval = float(str("VOLT:TRIG? (@{})".format(self.chan)).rstrip("\n"))

        sent = "The voltage trigger is set to: {} V.\n".format(self.volt_trigval)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.volt_trigval

    #===============================================================
    def curr_out(self, outval = None):
        """Set or examine the output current.

        Returns current output value in A.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        outval: output current [A] (must not exceed the set current range)
        """
        if outval == None:
            pass
        else:
            if float(outval)>self.curr_rangval_float:
                print("The entered output value exceeds the set current range, which is: {}\n".format(self.curr_rangval))
            else:
                self._dev.write('CURR {}, (@{})'.format(float(outval), self.chan))

        self.curr_outval = float(str(self._dev.query('CURR? (@{})'.format(self.chan))).rstrip('\n'))
        self.volt_outval = None
        sent = "The output current is set to: {} A.\n".format(self.curr_outval)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.curr_outval

    #===============================================================
    def curr_range(self, rang = None):
        """Set or examine the current range.

        Returns current range.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        range: current range (strings can be entered in uppercase)
        R1uA – 1e-6, '1u', '1 u', '1ua', '1 ua', 'r1ua'
        R10uA – 1e-5, '10u', '10 u', '10ua', '10 ua', 'r10ua'
        R100uA – 1e-4, '100u', '100 u', '100ua', '100 ua', 'r100ua'
        R1mA  – 1e-3, '1m', '1 m', '1ma', '1 ma', 'r1ma'
        R10mA – 1e-2, '10m', '10 m', '10ma', '10 ma', 'r10ma'
        R120mA – 12e-2, '120m', '120 m', '120ma', '120 ma', 'r120ma'
        (if nothing or 'None' is entered, the function will only examine the parameter)
        """
        if rang == None:
            pass
        elif (rang == 1e-6) or (str(rang).lower() in ['1e-6', '1u', '1 u', '1ua', '1 ua', 'r1ua']):
            self._dev.write("CURR:RANG R1uA, (@{})".format(self.chan))
        elif (rang == 1e-5) or (str(rang).lower() in ['1e-5', '10u', '10 u', '10ua', '10 ua', 'r10ua']):
            self._dev.write("CURR:RANG R10uA, (@{})".format(self.chan))
        elif (rang == 1e-4) or (str(rang).lower() in ['1e-4', '100u', '100 u', '100ua', '100 ua', 'r100ua']):
            self._dev.write("CURR:RANG R100uA, (@{})".format(self.chan))
        elif (rang == 1e-3) or (str(rang).lower() in ['1e-3', '1m', '1 m', '1ma', '1 ma', 'r1ma']):
            self._dev.write("CURR:RANG R1mA, (@{})".format(self.chan))
        elif (rang == 1e-2) or (str(rang).lower() in ['1e-2', '10m', '10 m', '10ma', '10 ma', 'r10ma']):
            self._dev.write("CURR:RANG R10mA, (@{})".format(self.chan))
        elif (rang == 12e-2) or (str(rang).lower() in ['12e-2', '120m', '120 m', '120ma', '120 ma', 'r120ma']):
            self._dev.write("CURR:RANG R120mA, (@{})".format(self.chan))

        self.curr_rangval = str(self._dev.query("CURR:RANG? (@{})".format(self.chan))).rstrip('\n')

        if self.curr_rangval == 'R1uA':
            self.curr_rangval_float = 1e-6
        elif self.curr_rangval == 'R10uA':
            self.curr_rangval_float = 1e-5
        elif self.curr_rangval == 'R100uA':
            self.curr_rangval_float = 1e-4
        elif self.curr_rangval == 'R1mA':
            self.curr_rangval_float = 1e-3
        elif self.curr_rangval == 'R10mA':
            self.curr_rangval_float = 1e-2
        elif self.curr_rangval == 'R120mA':
            self.curr_rangval_float = 12e-2

        sent = "The current range is set to: {}.\n".format(self.curr_rangval)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.curr_rangval_float

    #===============================================================
    def curr_limit(self, limit = None):
        """Set or examine the current limit.

        Returns current limit in A.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        limit: current limit [A] (must not exceed the set current range)
        """
        if limit == None:
            pass
        else:
            if (float(limit)>self.curr_rangval_float):
                print("The entered current limit exceeds the set current range, which is: {}\n".format(self.curr_rangval))
            else:
                self._dev.write("CURR:LIM {}, (@{})".format(float(limit),self.chan))

        self.curr_limitval = float(str(self._dev.query("CURR:LIM? (@{})".format(self.chan))).rstrip('\n'))

        sent = "The current limit is set to: {} A.\n".format(self.curr_limitval)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.curr_limitval

    #===============================================================
    def curr_trig(self, trig = None):
        """Set or examine the current trigger.

        Returns current trigger.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        trig: current trigger [A]
        """
        if trig == None:
            pass
        else:
            self._dev.write("CURR:TRIG {}, (@{})".format(float(trig), self.chan))

        self.curr_trigval = float(str("CURR:TRIG? (@{})".format(self.chan)).rstrip("\n"))

        sent = "The current trigger is set to: {} A.\n".format(self.curr_trigval)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.curr_trigval

    #===============================================================
    def output(self, output = None):
        """Set or examine if the output is on or off.

        Returns 1 if the output is on or 0 if the output is off.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        output: turn the output on or off
        ON - 1, '1', 'on', 'ON'
        OFF - 0, '0', 'off', 'OFF'
        """
        if output == None:
            pass
        elif output in [1, '1', 'on', 'ON']:
            self._dev.write("OUTP 1, (@{})".format(self.chan))
        elif output in [0, '0', 'off', 'OFF']:
            self._dev.write("OUTP 0, (@{})".format(self.chan))
        else:
            raise ValueError("Wrong input.\n")

        self.outputval = int(str(self._dev.query("OUTP? (@{})".format(self.chan))).rstrip('\n'))
        if self.outputval == 1:
            out = 'ON'
        elif self.outputval == 0:
            out = 'OFF'
        else:
            raise ValueError("Error.\n")

        sent = "Output is set to: {}\n".format(out)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return self.outputval

    #===============================================================
    def sweep_points(self, sp = None):
        """Set or examine the sweep points.

        Returns the number of sweep points.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        sp: number of points
        integer number 1-4096
        """
        if sp == None:
            pass
        elif (int(sp) in list(range(4097))) and (int(sp) != 0):
            self._dev.write("SENS:SWE:POIN {}, (@{})".format(sp, self.chan))
        else:
            raise ValueError("Wrong input.\n")

        sp = int(str(self._dev.query("SENS:SWE:POIN? (@{})".format(self.chan))).rstrip("\n"))
        sent = "The number of sweep points is: {}.\n".format(sp)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return sp

    #===============================================================
    def tinterval(self, time = None):
        """Set or examine the time interval between measurements.

        Returns time interval.

        Input parameters
        ----------------
        (if nothing or 'None' is entered, the function will only examine the parameter)
        time: time interval (in milliseconds)
        1 - 32767
        """
        if time == None:
            pass
        elif (float(time) in list(range(32768))) and (float(time) != 0):
            self._dev.write("SENS:SWE:TINT {}, (@{})".format(time, self.chan))
        else:
            raise ValueError("Wrong input.\n")

        time = float(str(self._dev.query("SENS:SWE:TINT? (@{})".format(self.chan))).rstrip("\n"))
        sent = "The time interval is: {} ms.\n".format(time)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return time

    #===============================================================
    def aper(self, typ):
        """Examine the voltage or current aperture.

        Returns aperture value in seconds.

        Input parameters
        ----------------
        typ: voltage or current aperture (uppercase may also be used in strings)
        voltage aperture - 1, '1', 'v', 'volt', 'voltage'
        current aperture - 2, '2', 'i', 'curr', 'current'
        """
        if (typ == 1) or (str(typ).lower() in ['1', 'v', 'volt', 'voltage']):
            typ_sent = 'voltage'
            aper = float(str(self._dev.query("SENS:VOLT:APER? (@{})".format(self.chan))).rstrip("\n"))
        elif (typ == 2) or (str(typ).lower()  in ['2', 'i', 'curr', 'current']):
            typ_sent = 'current'
            aper = float(str(self._dev.query("SENS:CURR:APER? (@{})".format(self.chan))).rstrip("\n"))
        else:
            raise ValueError("Wrong input.\n")

        sent = "The {} is: {} s.\n".format(typ_sent, aper)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return aper

    #===============================================================
    def nplc(self, typ, cyc = None):
        """Examine or set the NPLC parameter.

        Returns number of power line cycles taken for the measurement.

        Input parameters
        ----------------
        typ: number of cycles for voltage/current
        voltage aperture - 1, '1', 'v', 'volt', 'voltage'
        current aperture - 2, '2', 'i', 'curr', 'current'

        cyc: number of cycles (if nothing or 'None' is entered, the function will only examine the parameter)
        integer number 0-255
        """
        if cyc == None:
            pass
        elif cyc in list(range(256)):
            if (typ == 1) or (str(typ).lower() in ['1', 'v', 'volt', 'voltage']):
                typ_sent = 'voltage'
                typ = 'VOLT'
                self._dev.write("SENS:CURR:NPLC {}, (@{})".format(cyc, self.chan))
            elif (typ == 2) or (str(typ).lower() in ['2', 'i', 'curr', 'current']):
                typ_sent = 'current'
                typ = 'CURR'
                self._dev.write("SENS:CURR:NPLC {}, (@{})".format(cyc, self.chan))
            else:
                raise ValueError("Wrong input for variable typ.\n")
        else:
            raise ValueError("Wrong input for variable cyc.\n")

        cyc = int(str(self._dev.query("SENS:{}:NPLC? (@{})".format(typ, self.chan))).rstrip("\n"))

        sent = "The number of power cycles for the {} measurement is: {}.\n".format(typ_sent, cyc)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return cyc

    #===============================================================
    # PRIVATE METHODS
    #===============================================================
    def _sel_chan(self, chan = None):
        """Select channel.

        Input parameters
        ----------------
        chan: channel
        (1, 2, 3)

        """
        if chan == None:
            chan = int(input("Select a channel(1-3): "))
        if chan not in [1,2,3]:
            raise ValueError("Wrong input")

        self.chan = chan

        self._sent1 = str(self.name) + "\nTime: "
        self._sent2 = "\nAddress: " + str(self.addr) + "\nChannel: " + str(self.chan) + "\n\n"

        sent = "The selected channel is: {}\n".format(chan)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
