# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class KeysightE3649A(GPIB):
    """Voltage source Keysight E3649A.

    """
    #===============================================================
    def __init__(self, addr, channel, fname = None):
        """Initialization.

        Input parameters
        ----------------
        addr: what address to select
        channel: Which channel to select:
        1 or 'l' or 'left'; 2 or 'r' or 'right'.
        fname: name of the file where the output data will be written
        """
        rm = visa.ResourceManager()
        self._dev = rm.open_resource('GPIB0::' + str(addr) + '::INSTR')

        self.addr = addr
        self.fname = fname
        self.chan = channel

        # reset: outputs are off
        self._reset()

        # enable channel
        self.enable()

        # get instrument name
        self.name = self._name()

    #===============================================================
    def get_address(self):
        """Get the device's address.

        Returns the device's address.

        """
        return self.addr

    #===============================================================
    def get_channel(self):
        """Get the device's channel.

        Returns the device's channel.

        """
        return self.chan

    #===============================================================
    def enable(self, zero = True):
        """Enable channel.

        Input parameters
        ----------------
        zero: default value is True
        """
        # select channel
        self._sel()
        if zero:
            self._set_param(0, 0)
        self._dev.write('OUTP ON')

    #===============================================================
    def disable(self):
        """Disable channel.

        Input parameters
        ----------------
        channel: Which channel to select:
        1 or 'l' or 'left'; 2 or 'r' or 'right'.
        """
        self._dev.write('OUTP OFF')

    #===============================================================
    def set_both(self, volt, max_curr):
        """Set voltage or read voltage level.

           Set current or read current level.

           Returns the measured voltage and current.

        Input parameters
        ----------------
        volt: Voltage in volts [V].
        max_curr: Maximum current in ampers [A].
        """
        # select channel
        self._sel()

        U, I = self._set_param(volt, max_curr)

        return U, I

    #===============================================================
    def voltage(self, volt = None):
        """Set voltage or read voltage level.

           Returns the measured voltage.

        Input parameters
        ----------------
        channel: Which channel to select:
        1 or 'l' or 'left'; 2 or 'r' or 'right'.
        (optional) volt: Voltage in volts [V].

        """
        # select channel
        self._sel()

        if volt is None:
            U = float(self._dev.query('MEAS:VOLT?'))
            sentence = self._sent + "The measured voltage is: " + str(U) + "V.\n\n"
            print(sentence)
            self._write_sent(sentence)
            return U
        else:
            U, I = self._set_param(volt = volt)
            return U

    #===============================================================
    def current(self, max_curr = None):
        """Set current limit or read current level.

           Returns the measured current.

        Input parameters
        ----------------
        channel: Which channel to select:
        1 or 'l' or 'left'; 2 or 'r' or 'right'.
        (optional) max_curr: Maximum current in ampers [V].

        """
        # select channel
        self._sel()

        if max_curr is None:
            I = float(self._dev.query('MEAS:CURR?'))
            sentence = self._sent + "The measured current is: " + str(I) + "A.\n\n"
            print(sentence)
            self._write_sent(sentence)
            return I
        else:
            U, I = self._set_param(max_curr = max_curr)
            return I

    #===============================================================
    def set_range(self, rang = None):
        """Set the range to low or high.

        """
        # select channel
        self._sel()
        if rang is None:
            pass
        else:
            if rang in [1, 'l', 'low']:
                self._dev.write('VOLT:RANG LOW')
            elif rang in [2, 'h', 'high']:
                self._dev.write('VOLT:RANG HIGH')
            else:
                raise ValueError("Please select 1 ('l'; 'low') or 2 ('h'; 'high').\n")
        out = self._dev.query('VOLT:RANG?')
        if out.startswith('P35V'):
            sentence = self._sent + "Low range: 35V.\n\n"
            print(sentence)
            self._write_sent(sentence)
        elif out.startswith('P60V'):
            sentence = self._sent + "High range: 60V.\n\n"
            print(sentence)
            self._write_sent(sentence)
        else:
            raise ValueError("Wrong output from instrument.\n")

    #===============================================================
    def set_prot(self, prot = None, state = None):
        """Set the voltage level at which the overvoltage protection (OVP) circuit will trip.

        Input parameters
        ----------------
        (optional) prot: Set the voltage protection level in volts [V].
        (optional) state: Turn on overvoltage protection(1 or 'on') or
        turn off overvoltage protection(0 or 'off').

        """
        # select channel
        self._sel()

        if prot is None:
            pass
        else:
            if prot < 1 or prot > 66:
                raise ValueError("prot should be between 1 V and 66 V.")
            self._dev.write('VOLT:PROT ', '%f' % prot)
        out = self._dev.query('VOLT:PROT?')
        sentence = self._sent + "The overvoltage protection is set to:" + str(out) + "V.\n\n"
        print(sentence)
        self._write_sent(sentence)

        if state in [1, 'on']:
            self._dev.write('VOLT:PROT:STAT 1')
            sentence = self._sent + "Overvoltage protection is on.\n\n"
            print(sentence)
            self._write_sent(sentence)
        elif state in [0, 'off'] :
            self._dev.write('VOLT:PROT:STAT 0')
            sentence = self._sent + "Overvoltage protection is off.\n\n"
            print(sentence)
            self._write_sent(sentence)
        elif state == None:
            o = self._dev.query('VOLT:PROT:STAT?')
            if o.startswith('1'):
                sentence = self._sent + "Overvoltage protection is on.\n\n"
                print(sentence)
                self._write_sent(sentence)
            elif o.startswith('0'):
                sentence = self._sent + "Overvoltage protection is off.\n\n"
                print(sentence)
                self._write_sent(sentence)
            else:
                raise ValueError("Please make a valid input\n.")
        else:
            raise ValueError("Please make a valid input\n.")

    #===============================================================
##    def clear_prot(self):
##    """Cause the overvoltage protection circuit to be cleared.
##
##    """
##    self._dev.write('VOLT:PROT:CLE')
##    print("The overvoltage protection circuit has been cleared.\n")

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
    def _reset(self, sleeptime = 1):
        """Reset device.

           Returns the sleeptime.

        Input parameters
        ----------------
        sleeptime: sleep time in seconds
        (if nothing is entered, the default sleeptime is 1s)

        """
        self._dev.write('*RST')
        time.sleep(sleeptime)
        return sleeptime

    #===============================================================
    def _sel(self):
        """Select channel.

        """

        self._timestamp()

        self._sent = "Time: " + str(self.time) + "\nAddress: " + str(self.addr) + \
                     "\nChannel: " + str(self.chan) + "\n"

        if self.chan in [1, 'l', 'left']:
            self.chan = 1
            self._dev.write('INST:SEL OUT1')
        elif self.chan in [2, 'r', 'right']:
            self.chan = 2
            self._dev.write('INST:SEL OUT2')
        else:
            raise ValueError("Please select 1 ('l'; 'left') or 2 ('r'; 'right').\n")

    #===============================================================
    def _set_param(self, volt = None, max_curr = None, sleeptime = 0.3):

        """Set voltage limit and measure it.

           Returns the measured voltage and current.

        Input parameters
        ----------------.
        volt: Voltage in volts [V].
        max_curr: Maximum current in ampers [A].
        sleeptime: sleep time in seconds
        (if nothing is entered, the default sleeptime is 0.3s)

        """
        if volt is not None:
            self._dev.write('VOLT ', '%f' % volt)

        if max_curr is not None:
            self._dev.write('CURR ', '%f' % max_curr)

        time.sleep(sleeptime)

        U = float(self._dev.query('MEAS:VOLT?'))
        sentence = self._sent + "Voltage stabilized to " + str(U) + "V.\n\n"
        print(sentence)
        self._write_sent(sentence)
        I = float(self._dev.query('MEAS:CURR?'))
        sentence = self._sent + "Current stabilized to " + str(I) +  "A.\n\n"
        print(sentence)
        self._write_sent(sentence)

        return U, I

    #===============================================================
    def _write_sent(self, sentence):
        """Write a sentence in a file.

        Input parameters
        ----------------
        sentence: predetermined

        """
        with open(self.fname + ".txt", "a") as f:
            f.write(sentence)

    #===============================================================
    def _timestamp(self):
        """Creates a timestamp both in float and string format.

           Returns the created timestamp.

        """
        self.time_float = time.time()
        t0 = time.asctime(time.localtime(self.time_float))
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
        return timestr
