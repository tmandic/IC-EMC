# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

#===============================================================
class GPIB(object):
    """Base class for instruments.

    """

    #===============================================================
    def __init__(self):
        """Initialization function.

        """
        raise NotImplementedError

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
        name = name.rstrip('\r\n')
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
