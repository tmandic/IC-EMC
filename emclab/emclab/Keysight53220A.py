# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class Keysight53220A(GPIB):
    """Frequency counter Keysight 53220A.

    """
    #===============================================================
    def __init__(self, addr, chan = None, level = None, gatetime = None, trigcoun = None, fname = None):
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

        self.level = level

        self.gatetime = gatetime

        self.trigcoun = trigcoun

        self._sel_chan(chan = chan)

    #===============================================================
    def meas_freq(self):
        """Measure frequency.

        Returns frequency.
        """
        freq = float(self._dev.query(("MEAS:FREQ? (@{})").format(self.chan)))

        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2

        sent = "The measured frequency is: {} Hz.\n".format(freq)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return freq

    #===============================================================
    def meas_width(self, pul = None):
        """Measures signal width.

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
            width = float(self._dev.query(('MEAS:NWID? (@{})').format(self.chan)))
        elif pul in [2, '2', 'neg', 'negative', 'NEG', 'NEGATIVE']:
            width = float(self._dev.query(('MEAS:PWID? (@{})').format(self.chan)))
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
    def meas_duty_cycle(self):
        """Measure positive duty cycle.

        Returns positive duty cycle.

        """
        dc = float(self._dev.query(('MEAS:PDUT? (@{})').format(self.chan)))
        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The measured duty cycle is: {} %\n".format(dc)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return dc

    #===============================================================
    def meas_time_r(self, tim = None, llevel = None, ulevel = None):
        """Measures fall or rise time using the READ function.

        Returns fall or rise time.

        Input parameters
        ----------------
        tim: selects whether the measurement of fall or rise time
        fall time - 1, '1', 'f', 'F', 'fall', 'FALL', 'falltime', 'FALLTIME'
        rise time - 2, '2', 'r', 'R', 'rise', 'RISE', 'risetime', 'RISETIME'
        (if nothing is entered, fall time will be measured)

        llevel, ulevel:
        The llevel(<lower_reference>) and ulevel(<upper_reference>) parameters specify the input signal reference level,
        either in terms of percent of peak-to-peak voltage, or in absolute voltage. To specify the level in percent,
        use a numeric value with no suffix or with the PCT suffix; for example, 30 or 30 PCT. To specify the
        level in absolute voltage, use a numeric value with the V or MV (millivolt) suffix: 100 MV or .1V.
        If <lower_reference> is greater than <upper_reference>, no error is generated, but the measurement result
        is undefined.
        (if nothing is entered, default values will be used (llevel = 10, ulevel = 90))

        """
        if llevel == None:
            llevel = 10
        if ulevel == None:
            ulevel = 90
        if tim in [1, '1', 'f', 'F', 'fall', 'FALL', 'falltime', 'FALLTIME']:
            word = 'fall'
            time = float(self._dev.query("CONF:FTIM {},{},(@{})\nREAD?".format(llevel,ulevel, self.chan)))
        elif (tim == None) or (tim in [2, '2', 'r', 'R', 'rise', 'RISE', 'risetime', 'RISETIME']):
            word = 'rise'
            time = float(self._dev.query('CONF:RTIM {},{},(@{})\nREAD?'.format(llevel,ulevel,self.chan)))
        else:
            raise ValueError("Wrong input for the 'tim' parameter.\n")

        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2

        sent = "The measured {} time is: {} s.\n".format(word, time)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return time

    #===============================================================
    def meas_duty_cycle_r(self, pol = None, lev = None, coupling = None, mode = None):
        """Measures duty cycle.

        Returns duty cycle.

        Input parameters
        ----------------
        pol - selects positive or negative duty cycle
        positive - 1, '1', 'p', 'pos', 'positive', 'P', 'POS', 'POSITIVE'
        negative - 2, '2', 'n', 'neg', 'negative', 'N', 'NEG', 'NEGATIVE'
        (if nothing is entered, default values will be used ('p'))

        The lev(<reference>) parameter specifies the input signal reference level, either in terms of percent of peakto-
        peak voltage, or in absolute voltage. To specify the level in percent, use a numeric value with no suffix
        or with the PCT suffix; for example, 30 or 30 PCT. To specify the level in absolute voltage, use a
        numeric value with the V or MV (millivolt) suffix: 100 MV or .1V.
        When the lev(<reference>) is omitted or specified in percent, auto-leveling is enabled. When specified in
        absolute voltage, auto-leveling is disabled.
        (if nothing is entered, default values will be used (0 [v] or 50 PCT))

        coupling: select ac or dc coupling (used when mode is set to 1)
        ac - 1, '1', 'ac', 'AC'
        dc - 2, '2', 'dc', 'DC'
        (if nothing is entered, default values will be used('ac'))

        mode: selects whether the 'lev' variable(reference level) will be entered in % or in [V]
        % - 0, '0'
        [V] - 1, '1'
        (if nothing is entered, default values will be used(1))

        """
        if (pol == None) or (pol in [1, '1', 'p', 'pos', 'positive', 'P', 'POS', 'POSITIVE']):
            word = 'positive'
            dc_q = 'P'
        elif pol in [2, '2', 'n', 'neg', 'negative', 'N', 'NEG', 'NEGATIVE']:
            word = 'negative'
            dc_q = 'N'
        else:
            raise ValueError("Wrong input for the 'pol' parameter.\n")

        if (coupling == None) or (coupling in [1, '1', 'ac', 'AC']):
            coupling = 'AC'
        elif coupling in [2, '2', 'dc', 'DC']:
            coupling = 'DC'
        else:
            raise ValueError("Wrong input for the 'coupling' parameter.\n")

        if mode in [0, '0']:
            if lev != None:
                level = lev
            elif self.level != None:
                level = self.level
            elif lev == None:
                level = 50
            else:
                raise ValueError("Error.\n")
            if (level<10) or (level>90):
                raise ValueError("Wrong input for level.\n")
            dc = float(self._dev.query(('CONF:{}DUT {},(@{})\nREAD?').format(dc_q, level, self.chan)))
        elif (mode == None) or (mode in [1, '1']):
            if lev != None:
                level = lev
            elif lev == None:
                level = 0
            else:
                raise ValueError("Error.\n")
            width = float(self._dev.query(('CONF:{}DUT {}V,(@{})\nINP{}:COUP {}\nREAD?').format(dc_q, level, self.chan, self.chan, coupling)))
        else:
            raise ValueError("Wrong input for the 'mode' parameter.\n")

        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The measured {} duty cycle is: {} %.\n".format(word, (dc*100))
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return dc

    #===============================================================
    def meas_width_r(self, pol = None, lev = None, coupling = None, mode = None):
        """Measures positive signal width.

        Returns positive signal width.

        Input parameters
        ----------------
        pol: selects positive or negative signal width
        positive - 1, '1', 'p', 'pos', 'positive', 'P', 'POS', 'POSITIVE'
        negative - 2, '2', 'n', 'neg', 'negative', 'N', 'NEG', 'NEGATIVE'
        (if nothing is entered, default values will be used ('p'))

        lev:
        The lev(<reference>) parameter specifies the input signal reference level, either in terms of percent of peakto-
        peak voltage, or in absolute voltage. To specify the level in percent, use a numeric value with no suffix
        or with the PCT suffix; for example, 30 or 30 PCT. To specify the level in absolute voltage, use a
        numeric value with the V or MV (millivolt) suffix: 100 MV or .1V.
        (if nothing is entered, default values will be used (0 [V] or 50 PCT))

        coupling: select ac or dc coupling (used when mode is set to 1)
        ac - 1, '1', 'ac', 'AC'
        dc - 2, '2', 'dc', 'DC'
        (if nothing is entered, default values will be used('ac'))

        mode: selects whether the 'lev' variable(reference level) will be entered in % or in [V]
        % - 0, '0'
        [V] - 1, '1'
        (if nothing is entered, default values will be used(1))

        """
        if (pol == None) or (pol in [1, '1', 'p', 'pos', 'positive', 'P', 'POS', 'POSITIVE']):
            word = 'positive'
            width_q = 'P'
        elif pol in [2, '2', 'n', 'neg', 'negative', 'N', 'NEG', 'NEGATIVE']:
            word = 'negative'
            width_q = 'N'
        else:
            raise ValueError("Wrong input for the 'pol' parameter.\n")

        if (coupling == None) or (coupling in [1, '1', 'ac', 'AC']):
            coupling = 'AC'
        elif coupling in [2, '2', 'dc', 'DC']:
            coupling = 'DC'
        else:
            raise ValueError("Wrong input for the 'coupling' parameter.\n")

        if mode in [0, '0']:
            if lev != None:
                level = lev
            elif self.level != None:
                level = self.level
            elif lev == None:
                level = 50
            else:
                raise ValueError("Error.\n")
            if (level<10) or (level>90):
                raise ValueError("Wrong input for level.\n")
            width = float(self._dev.query(('CONF:{}WID {},(@{})\nREAD?').format(width_q, level, self.chan)))
        elif (mode == None) or (mode in [1, '1']):
            if lev != None:
                level = lev
            elif lev == None:
                level = 0
            else:
                raise ValueError("Error.\n")
            width = float(self._dev.query(('CONF:{}WID {}V,(@{})\nINP{}:COUP {}\nREAD?').format(width_q, level, self.chan, self.chan, coupling)))
        else:
            raise ValueError("Wrong input for the 'mode' parameter.\n")

        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The measured {} signal width is: {} s.\n".format(word, width)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return width

    #===============================================================
    def meas_freq_r(self, lev = None, ef = None, coupling = None, inpfilt = None, mode = None):
        """Measures frequency.

        Returns frequency.

        Input parameters
        ----------------
        lev: reference level
        number between 10 and 90 (in %) if mode in 0
        number in [V] if mode in 1
        (if nothing is entered, default values will be used(0 [V] / 50 PCT))

        ef: expected frequency
        number in [Hz]
        (if nothing is entered, default values will be used(1e6))

        coupling: select ac or dc coupling
        ac - 1, '1', 'ac', 'AC'
        dc - 2, '2', 'dc', 'DC'
        (if nothing is entered, default values will be used('ac'))

        inpfilt: enables or disables the input channel's low-pass filter. When enabled, the input channel is bandwidth-limited to 100 kHz.
        on - 1, '1', 'on', 'ON'
        off - 0, '0', 'off', 'OFF'
        (when nothing is entered, the input filter is set to 1)

        mode: selects whether the 'lev' variable(reference level) will be entered in % or in [V]
        % - 0, '0'
        [V] - 1, '1'
        (if nothing is entered, default values will be used(1))

        """
        if ef == None:
            ef = 1e6

        if (inpfilt == None) or (inpfilt in [1, '1', 'on', 'ON']):
            inpfilt = 'ON'
        elif inpfilt in [0, '0', 'off', 'OFF']:
            inpfilt = 'OFF'
        else:
            raise ValueError("Wrong input for the variable 'inpfilt'.\n")

        if (coupling == None) or (coupling in [1, '1', 'ac', 'AC']):
            coupling = 'AC'
        elif coupling in [2, '2', 'dc', 'DC']:
            coupling = 'DC'
        else:
            raise ValueError("Wrong input for the 'coupling' parameter.\n")

        if self.gatetime == None:
            self.gatetime = 0.1
        elif ((float(self.gatetime)<1e-4) or (float(self.gatetime)>1000)):
            raise ValueError("Wrong input for the variable gatetime")
        else:
            pass

        if self.trigcoun == None:
            self.trigcoun = 1
        elif ((int(self.trigcoun)<1) or (int(self.trigcoun)>1e6)):
            raise ValueError("Wrong input for the variable trigcoun")
        else:
            pass

        if ((self.gatetime>1)or (self.trigcoun>1)):
            timeout = self._dev.timeout
            self._dev.timeout = None

        if mode in [0, '0']:
            if lev != None:
                level = lev
            elif self.level != None:
                level = self.level
            elif lev == None:
                level = 50
            else:
                raise ValueError("Error.\n")
            if (level<10) or (level>90):
                raise ValueError("Wrong input for level.\n")
            self.level = level
            s = 'INP{}:COUP {}\nCONF:FREQ {},(@{})\nINP{}:LEV:AUTO ON\nINP{}:FILT {}\nINP{}:LEV:REL {}\nFREQ:GATE:SOUR TIME\nFREQ:GATE:TIME {}\nTRIG:COUN {}\nREAD?'.format(self.chan,coupling,ef,self.chan,self.chan,self.chan,inpfilt,self.chan,self.level,self.gatetime, self.trigcoun)
        elif (mode == None) or mode in [1, '1']:
            if lev != None:
                level = lev
            elif self.level != None:
                level = self.level
            elif lev == None:
                level = 0
            else:
                raise ValueError("Error.\n")
            self.level = level
            s = 'INP{}:COUP {}\nCONF:FREQ {},(@{})\nINP{}:FILT {}\nINP{}:LEV {}\nFREQ:GATE:SOUR TIME\nFREQ:GATE:TIME {}\nTRIG:COUN {}\nREAD?'.format(self.chan,coupling,ef,self.chan,self.chan,inpfilt,self.chan,self.level,self.gatetime, self.trigcoun)
        else:
            raise ValueError("Wrong input for the 'mode' parameter.\n")

        t1 = time.time()

        freq0 = self._dev.query(str(s))

        t2 = time.time()
        dt = t2-t1

        if (self.trigcoun == 1):
            freq = [float(freq0)]
            sent = "The measured frequency is: {} Hz.\n".format(freq)
        else:
            freq = [float(s) for s in freq0.split(",")]
            print("The measurement for\nN = {}\nand\nGatetime = {} s\ntook: {} s.\n".format(self.trigcoun,self.gatetime,dt))
            sent = "The measured frequencies are: {} Hz.\n".format(freq)

        if ((self.gatetime>1) or (self.trigcoun>1)):
            self._dev.timeout = timeout

        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return freq

    #===============================================================
    def meas_freq_ar(self, lev = None, ef = None, coupling = None, inpfilt = None):
        """Measures frequency.

        Returns frequency.

        Input parameters
        ----------------
        lev: reference level
        number in [V]
        (if nothing is entered, default values will be used(0))

        ef: expected frequency
        number in [Hz]
        (if nothing is entered, default values will be used(1e6))

        coupling: select ac or dc coupling
        ac - 1, '1', 'ac', 'AC'
        dc - 2, '2', 'dc', 'DC'
        (if nothing is entered, default values will be used('ac'))

        inpfilt: enables or disables the input channel's low-pass filter. When enabled, the input channel is bandwidth-limited to 100 kHz.
        on - 1, '1', 'on', 'ON'
        off - 0, '0', 'off', 'OFF'
        (when nothing is entered, the input filter is set to 1)

        """
        if ef == None:
            ef = 1e6

        if lev != None:
            level = lev
        elif lev == None:
            level = 0
        else:
            raise ValueError("Error.\n")

        if (inpfilt == None) or (inpfilt in [1, '1', 'on', 'ON']):
            inpfilt = 'ON'
        elif inpfilt in [0, '0', 'off', 'OFF']:
            inpfilt = 'OFF'
        else:
            raise ValueError("Wrong input for the variable 'inpfilt'.\n")

        if self.gatetime == None:
            self.gatetime = 0.1
        elif ((float(self.gatetime)<1e-4) or (float(self.gatetime)>1000)):
            raise ValueError("Wrong input for the variable gatetime")
        else:
            pass

        if (self.gatetime>1):
            timeout = self._dev.timeout
            self._dev.timeout = self.gatetime + 3000

        if (coupling == None) or (coupling in [1, '1', 'ac', 'AC']):
            s = 'INP{}:COUP AC\nCONF:FREQ {},(@{})\nINP{}:FILT {}\nINP{}:LEV {}\nFREQ:GATE:SOUR TIME\nFREQ:GATE:TIME {}\nREAD?'.format(self.chan,ef,self.chan,self.chan,inpfilt,self.chan,level,self.gatetime)
        elif coupling in [2, '2', 'dc', 'DC']:
            s = 'INP{}:COUP DC\nCONF:FREQ {},(@{})\nINP{}:FILT {}\nINP{}:LEV {}\nFREQ:GATE:SOUR TIME\nFREQ:GATE:TIME {}\nREAD?'.format(self.chan,ef,self.chan,self.chan,inpfilt,self.chan,level,self.gatetime)
        else:
            raise ValueError("Wrong input for the 'coupling' parameter.\n")

        freq = float(self._dev.query(str(s)))

        if (self.gatetime>1):
            self._dev.timeout = timeout

        self._timestamp()
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The measured frequency is: {} Hz.\n".format(freq)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return freq

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

        self._sent1 = str(self.name) + "\nTime: "
        self._sent2 = "\nAddress: " + str(self.addr) + "\nChannel: " + str(self.chan) + "\n\n"
        self._sent = self._sent1 + str(self.time) + self._sent2
        sent = "The selected channel is: {}\n".format(chan)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return chan
