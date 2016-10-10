# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class HP5385A(GPIB):
    """Frequency counter HP5385A.

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

        self._sent = "Time: " + str(self.time) + "\nAddress: " + str(self.addr) + "\n"

    #===============================================================
    def meas_freq(self):
        """Measure frequency.

        Returns frequency.

        """
        freq = self._dev.query("ENTER")

        print("The measured frequency is: {}\n".format(freq))

        return freq

    #===============================================================
    def get_address(self):
        """Get the device's address.

        """
        return self.addr

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
