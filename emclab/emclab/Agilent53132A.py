# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class Agilent53132A(GPIB):
    """Frequency counter Agilent 53132A.

    """
    #===============================================================
    def __init__(self, addr, chan = None, fname = None):
        """Initialization.

        """
        rm = visa.ResourceManager()
        self._dev = rm.open_resource('GPIB0::' + str(addr) + '::INSTR')

        # get instrument address

        self.addr = addr

        # get instrument name
        self.name = self._name()

        self._timestamp()

        self.fname = fname

        self._sel_chan(chan = chan)

    #===============================================================
    def meas_freq(self):
        """Measure frequency.

        Returns frequency.

        Input parameters
        ----------------
        chan - select channel:
        1, '1', 'A' or 2, '2', 'B'
        """
        self._dev.write("'FREQ {}'".format(self.chan))

        freq = float(self._dev.query("READ:FREQ?"))

        sent = "The measured frequency is: {} Hz.\n".format(freq)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return freq

    #===============================================================
    def set_attn(self, attn = None):
        """Sets attenuation to 1 or 10.

        Returns attenuation.

        Input parameters
        ----------------
        attn - atenuation level:
        1, '1' or 2, '2', 10, '10'
        """
        if attn == None:
            attn = int(input("Enter an attenuation level:\n1 - 1\n2 - 10\n"))

        if attn in [1,'1']:
            attn = 1
        elif attn in [2, '2', 10, '10']:
            attn = 10
        else:
            raise ValueError("Please enter a valid input\n")

        self._dev.write(':INP{}:ATT {}'.format(self.chan,attn))
        sent = "Attenuation has been set to: {}\n".format(attn)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
        self.meas_freq()

        return attn

    #===============================================================
    def set_filter(self, filt = None):
        """Enables or disables A-Input 100 kHz LPF.

        Returns filter status.

        Input parameters
        ----------------
        filt - filter turned on or off
        1, '1', 'off', 'Off', 'OFF' or 2, '2', 'on', 'On', 'ON'
        """

        if filt == None:
            filt = input("Turn A-Input 100kHz LPF:\n1 - OFF\n2 - ON\n")

        if filt in [1, '1', 'off', 'Off', 'OFF']:
            filt = 'OFF'
            filts = 0
        elif filt in [2, '2', 'on', 'On', 'ON']:
            filt = 'ON'
            filts = 1
        else:
            raise ValueError("Please enter a valid input\n")

        self._dev.write(':INPut{}:FILT {}'.format(self.chan, filts))
        sent = "A-Input 100 kHz LPF is set to: {}.\n".format(filt)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
        self.meas_freq()

        return filt

    #===============================================================
    # PRIVATE METHODS
    #===============================================================
    def _sel_chan(self, chan = None):
        """Select channel.

        Returns channel number.

        Input parameters
        ----------------
        chan - select channel:
        1, '1', 'A' or 2, '2', 'B'

        """
        if chan == None:
            chan = input("Select a channel:\n1 - A\n2 - B\n")

        if chan in [1,'1','A']:
            chan = 1
        elif chan in [2, '2', 'B']:
            chan = 2
        else:
            raise ValueError("Please enter a valid input\n")

        self.chan = chan

        self._sent = "Time: " + str(self.time) + "\nAddress: " + str(self.addr) + "\nChannel: " + str(self.chan) + "\n"

        sent = "The selected channel is: {}\n".format(chan)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return chan
