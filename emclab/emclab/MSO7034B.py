# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class MSO7034B(GPIB):
    """Mixed Signal Oscilloscope Keysight MSO7034B.

    """
    #===============================================================
    def __init__(self, addr, chan = None, fname = None):
        """Initialization.

        """
        rm = visa.ResourceManager()
        self._dev = rm.open_resource('USB0::' + str(addr) + '::INSTR')

        # get instrument address

        self.addr = addr

        # get instrument name
        self.name = self._name()

        self._timestamp()

        self.fname = fname

        self._sel_chan(chan = chan)

    #===============================================================
    def meas_freq(self):
        """Measure signal frequency.

        Returns signal frequency.
        """
        freq = float(self._dev.query(':MEAS:FREQ?'))
        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The measured frequency is: {} Hz\n".format(freq)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return freq

    #===============================================================
    def meas_duty_cycle(self):
        """Measure duty cycle.

        Returns duty cyle.

        """
        dc = float(self._dev.query(':MEAS:DUTY?'))
        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The measured duty cycle is: {} %\n".format(dc)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return dc

    #===============================================================
    def pwidth(self, freq = None):
        """Calculates positive signal width using measurements of the frequency
        and the duty cycle.
.
        Returns positive signal width.

        """
        dc = self.meas_duty_cycle()
        if freq == None:
            freq = self.meas_freq()
        pwidth = dc / (100 * freq)
        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The measured positive signal width is: {} s\n".format(pwidth)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return pwidth

    #===============================================================
    def meas_width(self, pul = None):
        """Measure signal width.

        Returns signal width.

        Input parameters
        ----------------
        pul: Measure positive or negative impulse:
        1, 'pos', 'positive'
        2, 'neg', 'negative'

        """
        if pul == None:
            pul= input("Do you want to measure the positive or the negative pulse:\n1 - POSITIVE\n2 - NEGATIVE\n")

        if pul in [1, '1', 'pos', 'positive', 'POS', 'POSITIVE']:
            width = float(self._dev.query(':MEASure:PWIDth?'))
        elif pul in [2, '2', 'neg', 'negative', 'NEG', 'NEGATIVE']:
            width = float(self._dev.query(':MEASure:NWIDth?'))
        else:
            raise ValueError("Error")
        self._timestamp()

        self._sent = self._sent1 + str(self.time) + self._sent2

        sent = "The measured width of the pulse is: {} s\n".format(width)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return width

    #===============================================================
    # PRIVATE METHODS
    #===============================================================
    def _sel_chan(self, chan = None):
        """Select channel.

        Input parameters
        ----------------
        chan: channel
        (1, 2, 3, 4)

        """
        if chan == None:
            chan = int(input("Select a channel(1-4): "))
        if chan not in [1,2,3,4]:
            raise ValueError("Wrong input")

        self.chan = chan

        self._sent1 = str(self.name) + "\nTime: "
        self._sent2 = "\nAddress: " + str(self.addr) + "\nChannel: " + str(self.chan) + "\n\n"

        self._dev.write(':MEASURE:SOURCE CHANNEL{}'.format(chan))
        sent = "The selected channel is: {}\n".format(chan)
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)
