# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

global adr
global chan

#===============================================================
class KeysightE3649A(GPIB):
    """Voltage source Keysight E3649A.

    """
    #===============================================================
    def __init__(self, adr):
        """Initialization.

        Input parameters
        ----------------
        adr: what adress to select

        """
        rm = visa.ResourceManager()
        self._dev = rm.open_resource('GPIB0::' + str(adr) + '::INSTR')

        self.adr = adr

        # reset: outputs are off
        self._reset()

        # enable channels 1, 2
        self.enable(1)
        self.enable(2)

        # get instrument name
        self.name = self._name()

    #===============================================================
    def ret_val(self):
        return self.adr

    #===============================================================

    def enable(self, channel, zero = True):
        """Enable channel.

        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        """
        self._sel(channel)
        if zero:
            self._set_param(channel, 0, 0)
        self._dev.write('OUTP ON')

    #===============================================================
    def disable(self, channel):
        """Disable channel.

        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        """
        self._sel(channel)
        self._dev.write('OUTP OFF')

    #===============================================================
    def set_both(self, channel, max_volt, max_curr):
        """Set voltage or read voltage level.

           Set current or read current level.


        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        max_volt: Maximum voltage in volts [V].
        max_curr: Maximum current in ampers [A].
        """
        # select channel
        self._sel(channel)

        self._set_param(channel, max_volt, max_curr)

    #===============================================================
    def voltage(self, channel, max_volt = None):
        """Set voltage or read voltage level.

        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        (optional) max_volt: Maximum voltage in volts [V].

        """
        # select channel
        self._sel(channel)

        if max_volt is None:
            U = float(self._dev.query('MEAS:VOLT?'))
            print("\nThe measured voltage is: ", '%f' % U, "V.\n")
            return U
        else:
            max_curr = None
            U = self._set_param(channel, max_volt, max_curr)
            return U

    #===============================================================
    def current(self, channel, max_curr = None):
        """Set current limit or read current level.

        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        (optional) max_curr: Maximum current in ampers [V].

        """
        # select channel
        self._sel(channel)

        if max_curr is None:
            I = float(self._dev.query('MEAS:CURR?'))
            print("\nThe measured current is: ", '%f' % I, "A.\n")
            return I
        else:
            max_volt = None
            I = self._set_param(channel, max_volt, max_curr)
            return I

    #===============================================================
    def set_range(self, channel, rang = None):
        """Set the range to low or high.

        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        (optional) rang: set the range to low or high

        """
        # select channel
        self._sel(channel)

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
            print("Low range: 35V.\n")
        elif out.startswith('P60V'):
            print("High range: 60V.\n")
        else:
            raise ValueError("Please select 1 ('l'; 'low') or 2 ('h'; 'high').\n")

    #===============================================================
    def set_prot(self, channel, prot = None, state = None):
        """Set the voltage level at which the overvoltage protection (OVP) circuit will trip.

        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        (optional) prot: Set the voltage protection level in volts [V].
        (optional) state: Turn on overvoltage protection(1 or 'on') or
        turn off overvoltage protection(0 or 'off').

        """
        # select channel
        self._sel(channel)

        if prot is None:
            pass
        else:
            self._dev.write('VOLT:PROT ', '%f' % prot)
        out = self._dev.query('VOLT:PROT?')
        print("The overvoltage protection is set to:", out, "V.\n")

        if state in [1, 'on']:
            self._dev.write('VOLT:PROT:STAT 1')
            print("Overvoltage protection is on.\n")
        elif state in [0, 'off'] :
            self._dev.write('VOLT:PROT:STAT 0')
            print("Overvoltage protection is off.\n")
        elif state == None:
            o = self._dev.query('VOLT:PROT:STAT?')
            if o.startswith('1'):
                print("Overvoltage protection is on.\n")
            elif o.startswith('0'):
                print("Overvoltage protection is off.\n")
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
    def _reset(self):
        """Reset device.

        """
        self._dev.write('*RST')

    #===============================================================
    def _sel(self, channel):
        """Select channel.

        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        """

        if channel in [1, 'l', 'left']:
            self._dev.write('INST:SEL OUT1')
        elif channel in [2, 'r', 'right']:
            self._dev.write('INST:SEL OUT2')
        else:
            raise ValueError("Please select 1 ('l'; 'left') or 2 ('r'; 'right').")

    #===============================================================
    def _set_param(self, channel, max_volt, max_curr):

        """Set maximum voltage and measure it.

        Input parameters
        ----------------
        channel: Which channel to select:
        (1 or 'l' or 'left'; 2 or 'r' or 'right').
        max_volt: Maximum voltage in volts [V].
        max_curr: Maximum current in ampers [A].

        """
        time.sleep(3)

        if max_volt is not None:
            self._dev.write('VOLT ', '%f' % max_volt)

        if max_curr is not None:
            self._dev.write('CURR ', '%f' % max_curr)

        time.sleep(0.3)

        U = float(self._dev.query('MEAS:VOLT?'))
        print("Voltage stabilized to ", U, "V.")
        I = float(self._dev.query('MEAS:CURR?'))
        print("Current stabilized to ", I, "A.")
