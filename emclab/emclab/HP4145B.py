# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from emclab import MSO7034B

from .GPIB import GPIB

#===============================================================
class HP4145B(GPIB):
    """Semiconductor Parameter Analyzer HP/Agilent 4145B.

    """
    #===============================================================
    def __init__(self, addr, fname = None, cd = None, channum = None,
                 vname = None, sourcefunction = None,
                 iname = None, sourcemode = None):
        """Initialization.

        Input parameters
        ----------------
        address: the device's address

        (OPTIONAL)
        cd: choose the type of channel:
        1 or '1' or 'smu' or 'SMU' for SMU;
        2 or '2' or 'VS' or 'Vs' or 'vs' for Vs;
        3 or '3' or 'VM' or 'Vm' or 'Vm' for Vm;

        channum: channel number:
        for SMU: 1-4
        for Vs: 1-2
        for Vm: 1-2

        vname: voltage name (up to 6 characters, have to upper case, may include numbers)

        (SMU) iname: current name (up to 6 characters, have to upper case, may include numbers)

        (SMU) sourcemode: source mode:
        1: V
        2: I
        3: COM (when sourcemode is set to 3, sourcefunction must be set to 3(CONST))

        (SMU and Vs) sourcefunction: source function:
        1: VAR1
        2: VAR2
        3: CONST
        4: VAR1'

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

        self.start()

        self.chan_def(cd = cd, channum = channum, vname = vname, sourcefunction = sourcefunction, iname = iname, sourcemode = sourcemode)

    #===============================================================
    def chan_def(self, cd = None, channum = None, vname = None, sourcefunction = None, iname = None, sourcemode = None):
        """Channel definition.

        Input parameters
        ----------------
        cd: choose the type of channel:
        1 or '1' or 'smu' or 'SMU' for SMU;
        2 or '2' or 'VS' or 'Vs' or 'vs' for Vs;
        3 or '3' or 'VM' or 'Vm' or 'Vm' for Vm;

        channum: channel number:
        for SMU: 1-4
        for Vs: 1-2
        for Vm: 1-2

        vname: voltage name (up to 6 characters)

        (SMU and Vs) sourcefunction: source function:
        1: VAR1
        2: VAR2
        3: CONST
        4: VAR1'

        (SMU) iname: current name (up to 6 characters)

        (SMU) sourcemode: source mode:
        1: V
        2: I
        3: COM (when sourcemode is set to 3, sourcefunction must be set to 3(CONST))

        """
        if cd == None:
            cd = input("Select:\n1 - SMU\n2 - Vs\n3 - Vm\n")

        self.cd = cd

        self.channum = None
        self.vname = None
        self.iname = None
        self.sourcemode = None
        self.sourcefunction = None

        if cd in ['SMU', 'smu', '1', 1]:
            cd_a = 'SMU'
            self._smu_def(channum = channum, vname = vname, sourcefunction = sourcefunction, iname = iname, sourcemode = sourcemode)
        elif cd in ['VS', 'Vs', 'vs', '2', 2]:
            cd_a = 'Vs'
            self._vs_def(channum = channum, vname = vname, sourcefunction = sourcefunction)
        elif cd in ['VM', 'Vm', 'vm', '3', 3]:
            cd_a = 'Vm'
            self._vm_def(channum = channum, vname = vname)
        else:
            raise ValueError("Wrong input.\n")

        self._timestamp()

        sent = "Channel {} - {} defined with the following parameters:\nVoltage name: {}".format(cd_a, self.channum, self.vname)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        if self.iname != None:
            sent = "Current name: {}".format(self.iname)
            print(sent)
            if self.fname != None:
                self._write_sent(sentence)

        if self.sourcemode != None:
            if self.sourcemode in [1, "1", "v", "V"]:
                sourcemode = "1: V"
            elif self.sourcemode in [2, "2", "i", "I"]:
                sourcemode = "2: I"
            elif self.sourcemode in [3, "3", "com", "COM"]:
                sourcemode = "3: COM"
            else:
                raise ValueError("Wrong input\n")
            sent = "Source mode: {}".format(sourcemode)
            print(sent)
            if self.fname != None:
                self._write_sent(sentence)

        if self.sourcefunction != None:
            if self.sourcefunction in [1, "1", "VAR1", "var1"]:
                sourcefunction = "1: VAR1"
            elif self.sourcefunction in [2, "2", "VAR2", "var2"]:
                sourcefunction = "2: VAR2"
            elif self.sourcefunction in [3, "3", "CONST", "const"]:
                sourcefunction = "3: CONST"
            elif self.sourcefunction in [4, "4", "VAR1'", "var1'"]:
                sourcefunction = "4: VAR1'"
            else:
                raise ValueError("Wrong input\n")
            sent = "Source function: {}".format(sourcefunction)
            print(sent)
            if self.fname != None:
                self._write_sent(sentence)

        print("\n")
        if self.fname != None:
            self._write_sent("\n")

    #===============================================================
    def source_setup(self, sourcemode = None, sweepmode = None, startval = None, stopval = None,
                     stepval = None, nusteps = None, compval = None, outval = None):
        """Set up the source.

        Input parameters
        ----------------
        (Setup for VAR1, VAR2, CONSTANT SMU): sourcemode: Source mode:
        Voltage Source: 1, "1", "v", "V"
        Current Source: 2, "2", "i", "I"

        (Setup for VAR1) sweepmode: sweep mode:
        1: LINEAR
        2: LOG 10
        3: LOG 25
        4: LOG 50

        (Setup for VAR1, VAR2) startval: start value

        (Setup for VAR1) stopval: stop value

        (Setup for VAR1, VAR2) stepval: step value

        (Setup for VAR2) nusteps: number of steps

        (Setup for VAR1, VAR2, CONSTANT SMU) compval: compliance value

        (Setup for CONSTANT SMU, CONSTANT Vs) outval: output value

        """

        self.sourcemode_ss = None
        self.sweepmode = None
        self.startval = None
        self.stopval = None
        self.stepval = None
        self.nusteps = None
        self.compval = None
        self.outval = None

        if self.sourcefunction in ["VAR1", "var1", "1", 1]:
            sf = "VAR1"
            self._source_setup_var1(sourcemode = sourcemode, sweepmode = sweepmode, startval = startval,
                                    stopval = stopval, stepval = stepval, compval = compval)
        elif self.sourcefunction in ["VAR2", "var2", "2", 2]:
            sf = "VAR2"
            self._source_setup_var2(sourcemode = sourcemode, startval = startval,
                                    stepval = stepval, nusteps = nusteps, compval = compval)
        elif self.sourcefunction in ["const", "CONST", "3", 3]:
            sf = "CONST"
            if self.cd in ['SMU', 'smu', "1", 1]:
                self._source_setup_const_smu(sourcemode = sourcemode, compval = compval, outval = outval)
            elif self.cd in ['VS', 'Vs', 'vs', "2", 2]:
                self._source_setup_const_vs(outval = outval)
            else:
                raise ValueError("Error")
        else:
            raise ValueError("Error")

        self._timestamp()

        if self.sourcemode_ss in [1, "1", "v", "V"]:
            sent = "Source {} - {} is set up with the following parameters:".format(self.vname, sf)
        elif self.sourcemode_ss in [2, "2", "i", "I"]:
            sent = "Source {} - {} is set up with the following parameters:".format(self.iname, sf)
        else:
            sent = "Source {} is set up with the following parameters:".format(sf)

        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        if self.sourcemode_ss != None:
            if self.sourcemode_ss in [1, "1", "v", "V"]:
                sourcemode = '1: V'
            elif self.sourcemode_ss in [2, "2", "i", "I"]:
                sourcemode = '2: I'
            else:
                raise ValueError("Wrong input\n")
            sent = "Source mode: {}".format(sourcemode)
            print(sent)
            if self.fname != None:
                self._write_sent(sentence)

        if self.sweepmode != None:
            if self.sweepmode in [1, "1", "LINEAR", "linear"]:
                sweepmode = "1: LINEAR"
            elif self.sweepmode in [2, "2", "LOG 10", "log 10", "LOG10", "log10"]:
                sweepmode = "2: LOG 10"
            elif self.sweepmode in [3, "3", "LOG 25", "log 25", "LOG25", "log25"]:
                sweepmode = "3: LOG 25"
            elif self.sweepmode in [4, "4", "LOG 50", "log 50", "LOG50", "log50"]:
                sweepmode = "4: LOG 50"
            else:
                raise ValueError("Wrong input\n")
            sent = "Sweep mode: {}".format(sweepmode)
            print(sent)
            if self.fname != None:
                self._write_sent(sent)

        if self.startval != None:
            sent = "Start value: {}".format(self.startval)
            print(sent)
            if self.fname != None:
                self._write_sent(sent)

        if self.stopval != None:
            sent = "Stop value: {}".format(self.stopval)
            print(sent)
            if self.fname != None:
                self._write_sent(sent)

        if self.stepval != None:
            sent = "Step value: {}".format(self.stepval)
            print(sent)
            if self.fname != None:
                self._write_sent(sentence)

        if self.nusteps != None:
            sent = "Number of steps: {}".format(self.nusteps)
            print(sent)
            if self.fname != None:
                self._write_sent(sentence)

        if self.outval != None:
            sent = "Output value: {}".format(self.outval)
            print(sent)
            if self.fname != None:
                self._write_sent(sent)

        if self.compval != None:
            sent = "Compliance value: {}".format(self.compval)
            print(sent)
            if self.fname != None:
                self._write_sent(sent)

        print("\n")
        if self.fname != None:
            self._write_sent("\n")

    #===============================================================
    def measure(self, me = None, osc = None, osc1 = None, osc2 = None):
        """Set the integration time.

        Input parameters
        ----------------
        me: measure mode:
        1 - SINGLE
        2 - REPEAT
        3 - APPEND
        4 - STOP

        param: parameter name you want to measure:
        voltage name or current name (if available)

        osc: optional parameter in case outer frequency meter devices are being used
        [1, '1', 'on', 'ON'] - enabled

        osc1 - optional - outer frequency meter
        osc2 - optional - outer frequency meter

        """
        if me == None:
            me = input("Select:\n1 - SINGLE\n2 - REPEAT\n3 - APPEND\n4 - STOP\n")

        if me in [1, "1", "single", "SINGLE"]:
            me = 1
            me_a = "SINGLE"
        elif me in [2, "2", "repeat", "REPEAT"]:
            me = 2
            me_a = "REPEAT"
        elif me in [3, "3", "append", "APPEND"]:
            me = 3
            me_a = "APPEND"
        elif me in [4, "4", "stop", "STOP"]:
            me = 4
            me_a = "STOP"
        else:
            raise ValueError("Wrong input\n")

        if self.iname == None:
            param = self.vname
        elif self.iname != None:
            if self.sourcemode_ss in [1, "1", "v", "V"]:
                param = self.iname
            elif self.sourcemode_ss in [2, "2", "i", "I"]:
                param = self.vname
        else:
            raise ValueError("Error\n")

        self.param = param

        if osc not in [1, '1', 'on', 'ON']:
            osc1 = None
            osc2 = None

        self._timestamp()
        sent = "Measuring of {} started in mode: {}\n".format(param, me_a)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        self._dev.write("MD ME{}".format(me))

        ts = self.nureadings*self.interval + self.wait + 1

        time.sleep(ts)

        if (me == 2) and (osc in [1, '1', 'on', 'ON']):
            f1 = osc1.meas_freq()
            f2 = osc2.meas_freq()
            testtime1 = time.time()
            time.sleep(10)
            while (((abs(osc1.meas_freq() - f1)) / f1)>10**(-3)) and (((abs(osc2.meas_freq()-f1))/f1)>10**(-3)):
                f1 = osc1.meas_freq()
                f2 = osc2.meas_freq()
                time.sleep(5)
                testtime2 = time.time()
                if ((testtime2-testtime1)>60):
                    print("Stabilization took longer than a minute, break program.\n")
                    break
            self._dev.write("MD ME4")

        self._timestamp()
        sent = "Measuring done.\n"
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

    #===============================================================
    def get_res(self):
        """Get the result of the measuring.

        Returns measurement.

        """

        if self.iname == None:
            param = self.vname
        elif self.iname != None:
            if self.sourcemode_ss in [1, "1", "v", "V"]:
                param = self.iname
            elif self.sourcemode_ss in [2, "2", "i", "I"]:
                param = self.vname
        else:
            raise ValueError("Error\n")

        self.param = param

        self._dev.write("DO '{}'".format(self.param))

        time.sleep(1)

        string = self._dev.query("ENTER")

        time.sleep(1)

        out = self._format_res(string)

        self._timestamp()
        sent = "The measurement of {} gave the following results:\n{}\n".format(self.param, out)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return out

    #===============================================================
    def turn_off_chan(self, cd = None, channum = None):
        """Turn of a channel.

        Input parameters
        ----------------
        cd: type of channel
        channum: channel number

        """
        if cd == None:
            cd = input("Select:\n1 - SMU\n2 - Vs\n3 - Vm\n")

        if channum == None:
            channum = int(input("Enter the channel number (1-4): "))
        if channum not in [1, 2, 3, 4]:
            raise ValueError("Wrong input\n")

        if cd in ['SMU', 'smu', '1', 1]:
            self._dev.write("DE CH{}".format(channum))
        elif cd in ['VS', 'Vs', 'vs', '2', 2]:
            self._dev.write("DE VS{}".format(channum))
        elif cd in ['VM', 'Vm', 'vm', '3', 3]:
            self._dev.write("DE VM{}".format(channum))
        else:
            raise ValueError("Wrong input.\n")

        self._timestamp()
        sent = "Channel {}-{} turned of.\n".format(cd, channum)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

    #===============================================================
    def start(self, it = 1, ca = 1, dr = 0):
        """Set up the wanted starting properties including integration time, auto calibration and the data ready bit.
        Clear the data output buffer after the previous operations.

        Input parameters
        ----------------
        it: integration time:
        1 - IT1/SHORT
        2 - IT2/MEDIUM
        3 - IT3/LONG
        default: 1 - IT1/SHORT

        ca: calibration:
        0 - OFF
        1 - ON
        default: 1 - ON

        dr: data ready:
        0 - OFF
        1 - ON
        default: 0 - OFF

        """
        time.sleep(2)
        self.integration_time(it = it)
        self.calibration(ca = ca)
        self.data_ready(dr = dr)
        self.buffer_clear()

        self._timestamp()
        sent = "Started the device.\n"
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

    #===============================================================
    def integration_time(self, it = None):
        """Set the integration time.

        Input parameters
        ----------------
        it: integration time:
        1 - IT1/SHORT
        2 - IT2/MEDIUM
        3 - IT3/LONG

        """
        if it == None:
            it = input("Select an integration time:\n1 - IT1/SHORT\n2 - IT2/MEDIUM\n3 - IT3/LONG\n")

        self.it = it

        if it in [1, "1", "it1", "IT1", "short", "SHORT"]:
            it = 1
            it_a = "IT1/SHORT"
        elif it in [2, "2", "it2", "IT2", "medium", "MEDIUM", "MED", "med"]:
            it = 2
            it_a = "IT2/MEDIUM"
        elif it in [3, "3", "it3", "IT3", "LONG", "long"]:
            it = 3
            it_a = "IT3/LONG"
        else:
            raise ValueError("Wrong input\n")

        self._dev.write("IT{}".format(it))
        self._timestamp()
        sent = "Integration time has been set to mode: {}\n".format(it_a)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

    #===============================================================
    def calibration(self, ca = None):
        """Set the auto calibration on or off.

        Input parameters
        ----------------
        ca: calibration:
        0 - OFF
        1 - ON

        """
        if ca == None:
            ca = int(input("Auto calibration:\n0 - OFF\n1 - ON\n"))

        if ca in ["off", "OFF", "0", 0]:
            ca = 0
            ca_a = "OFF"
        elif ca in ["on", "ON", "1", 1]:
            ca = 1
            ca_a = "ON"
        else:
            raise ValueError("Wrong input\n")

        self._dev.write("CA{}".format(ca))
        self._timestamp()
        sent = "Auto calibration is {}\n".format(ca_a)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

    #===============================================================
    def data_ready(self, dr):
        """Data ready option.

        Input parameters
        ----------------
        dr: data ready:
        0 - OFF
        1 - ON

        """
        if dr == None:
            dr = int(input("Data ready:\n0 - OFF\n1 - ON\n"))

        if dr in ["off", "OFF", "0", 0]:
            dr = 0
        elif dr in ["on", "ON", "1", 1]:
            dr = 1
        else:
            raise ValueError("Wrong input\n")

        self._dev.write("DR{}".format(dr))

    #===============================================================
    def buffer_clear(self):
        """Clears the data output buffer.

        """
        self._dev.write("BC")
        self._timestamp()
        sent = "Data output buffer cleared.\n"
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

    #===============================================================
    # PRIVATE METHODS
    #===============================================================
    def _smu_def(self, channum = None, vname = None, sourcefunction = None, iname = None, sourcemode = None):
        """Channel definition FOR smu.

        Input parameters
        ----------------
        cd: choose the type of channel:
        1 or '1' or 'smu' or 'SMU' for SMU;
        2 or '2' or 'VS' or 'Vs' or 'vs' for Vs;
        3 or '3' or 'VM' or 'Vm' or 'Vm' for Vm;

        channum: channel number:
        for SMU: 1-4
        for Vs: 1-2
        for Vm: 1-2

        vname: voltage name (up to 6 characters)

        (SMU and Vs) sourcefunction: source function:
        1: VAR1
        2: VAR2
        3: CONST
        4: VAR1'

        (SMU) iname: current name (up to 6 characters)

        (SMU) sourcemode: source mode:
        1: V
        2: I
        3: COM (when sourcemode is set to 3, sourcefunction must be set to 3(CONST))

        """
        if channum == None:
            channum = int(input("Enter the channel number (1-4): "))
        if channum not in [1, 2, 3, 4]:
            raise ValueError("Wrong input\n")
        self.channum = channum

        if vname == None:
            vname = input("Enter the voltage name (up to 6 characters): ")
        if len(vname)>6:
            raise ValueError("The voltage name is too long\n")
        self.vname = vname.upper()

        if iname == None:
            iname = input("Enter the current name(up to 6 characters): ")
        if len(iname)>6:
            raise ValueError("The current name is too long\n")
        self.iname = iname.upper()

        if sourcemode == None:
            sourcemode = input("Enter the source mode: ")
        self.sourcemode = sourcemode
        if sourcemode in [1, "1", "v", "V"]:
            sourcemode = 1
        elif sourcemode in [2, "2", "i", "I"]:
            sourcemode = 2
        elif sourcemode in [3, "3", "com", "COM"]:
            sourcemode = 3
        else:
            raise ValueError("Wrong input\n")

        if sourcefunction == None:
            sourcefunction = input("Enter the source function: ")
        self.sourcefunction = sourcefunction
        if sourcefunction in [1, "1", "VAR1", "var1"]:
            sourcefunction = 1
        elif sourcefunction in [2, "2", "VAR2", "var2"]:
            sourcefunction = 2
        elif sourcefunction in [3, "3", "CONST", "const"]:
            sourcefunction = 3
        elif sourcefunction in [4, "4", "VAR1'", "var1'"]:
            sourcefunction = 4
        else:
            raise ValueError("Wrong input\n")

        if sourcemode == 3:
            if sourcefunction != 3:
                raise ValueError("If source mode is set to COM, the source function must be se to CONST\n")

        self._dev.write("DE CH{},'{}','{}',{},{}".format(channum, self.vname, self.iname, sourcemode, sourcefunction))

    #===============================================================
    def _vs_def(self, channum = None, vname = None, sourcefunction = None):
        """Channel definition for Vs.

        Input parameters
        ----------------
        cd: choose the type of channel:
        1 or '1' or 'smu' or 'SMU' for SMU;
        2 or '2' or 'VS' or 'Vs' or 'vs' for Vs;
        3 or '3' or 'VM' or 'Vm' or 'Vm' for Vm;

        channum: channel number:
        for SMU: 1-4
        for Vs: 1-2
        for Vm: 1-2

        vname: voltage name (up to 6 characters)

        (SMU and Vs) sourcefunction: source function:
        1: VAR1
        2: VAR2
        3: CONST
        4: VAR1'

        (SMU) iname: current name (up to 6 characters)

        (SMU) sourcemode: source mode:
        1: V
        2: I
        3: COM (when sourcemode is set to 3, sourcefunction must be set to 3(CONST))

        """
        if channum == None:
            channum = int(input("Enter the channel number (1-2): "))
        if channum not in [1, 2]:
            raise ValueError("Wrong input\n")
        self.channum = channum

        if vname == None:
            vname = input("Enter the voltage name (up to 6 characters): ")
        if len(vname)>6:
            raise ValueError("The voltage name is too long\n")
        self.vname = vname.upper()

        if sourcefunction == None:
            sourcefunction = input("Enter the source function: ")
        self.sourcefunction = sourcefunction
        if sourcefunction in [1, "1", "VAR1", "var1"]:
            sourcefunction = 1
        elif sourcefunction in [2, "2", "VAR2", "var2"]:
            sourcefunction = 2
        elif sourcefunction in [3, "3", "CONST", "const"]:
            sourcefunction = 3
        elif sourcefunction in [4, "4", "VAR1'", "var1'"]:
            sourcefunction = 4
        else:
            raise ValueError("Wrong input\n")

        self._dev.write("DE VS{},'{}',{}".format(channum, self.vname, sourcefunction))

    #===============================================================
    def _vm_def(self, channum = None, vname = None):
        """Channel definition for Vm.

        Input parameters
        ----------------
        cd: choose the type of channel:
        1 or '1' or 'smu' or 'SMU' for SMU;
        2 or '2' or 'VS' or 'Vs' or 'vs' for Vs;
        3 or '3' or 'VM' or 'Vm' or 'Vm' for Vm;

        channum: channel number:
        for SMU: 1-4
        for Vs: 1-2
        for Vm: 1-2

        vname: voltage name (up to 6 characters)

        (SMU and Vs) sourcefunction: source function:
        1: VAR1
        2: VAR2
        3: CONST
        4: VAR1'

        (SMU) iname: current name (up to 6 characters)

        (SMU) sourcemode: source mode:
        1: V
        2: I
        3: COM (when sourcemode is set to 3, sourcefunction must be set to 3(CONST))

        """
        if channum == None:
            channum = int(input("Enter the channel number (1-4): "))
        if channum not in [1, 2]:
            raise ValueError("Wrong input\n")
        self.channum = channum

        if vname == None:
            vname = input("Enter the voltage name (up to 6 characters): ")
        if len(vname)>6:
            raise ValueError("The voltage name is too long\n")
        self.vname = vname.upper()

        self._dev.write("DE VM{},'{}'".format(channum, self.vname))

    #===============================================================
    def _source_setup_var1(self, sourcemode = None, sweepmode = None, startval = None, stopval = None, stepval = None, compval = None):
        """Set up VAR1.

        Input parameters
        ----------------
        (Setup for VAR1, VAR2, CONSTANT SMU): sourcemode: Source mode:
        Voltage Source: 1, "1", "v", "V"
        Current Source: 2, "2", "i", "I"

        (Setup for VAR1) sweepmode: sweep mode:
        1: LINEAR
        2: LOG 10
        3: LOG 25
        4: LOG 50

        (Setup for VAR1, VAR2) startval: start value

        (Setup for VAR1) stopval: stop value

        (Setup for VAR1, VAR2) stepval: step value

        (Setup for VAR2) nusteps: number of steps

        (Setup for VAR1, VAR2, CONSTANT SMU) compval: compliance value

        (Setup for CONSTANT SMU, CONSTANT Vs) outval: output value

        """
        if (self.sourcemode != None) and (self.sourcemode not in [3, "3", "com", "COM"]):
            self.sourcemode_ss = self.sourcemode
            sourcemode = self.sourcemode

        if sourcemode == None:
            sourcemode = input("Enter the source mode: ")
            self.sourcemode_ss = sourcemode
        if sourcemode in [1, "1", "v", "V"]:
            sourcemode = 'VR'
        elif sourcemode in [2, "2", "i", "I"]:
            sourcemode = 'IR'
        else:
            raise ValueError("Wrong input\n")

        if (self.sourcemode != None):
            if self.sourcemode in [1, "1", "v", "V"]:
                sourcemode_a = 'VR'
            elif self.sourcemode in [2, "2", "i", "I"]:
                sourcemode_a = 'IR'
            else:
                raise ValueError("Error\n")
            if (sourcemode != sourcemode_a):
                raise ValueError("Source mode defined in channel definition and source mode defined in source setup don't match.\n")

        if sweepmode == None:
            sweepmode = input("Select sweep mode:\n1 - LINEAR\n2 - LOG 10\n3 - LOG 25\n4 - LOG 50\n")

        self.sweepmode = sweepmode
        if sweepmode in [1, "1", "LINEAR", "linear"]:
            sweepmode = 1
        elif sweepmode in [2, "2", "LOG 10", "log 10", "LOG10", "log10"]:
            sweepmode = 2
        elif sweepmode in [3, "3", "LOG 25", "log 25", "LOG25", "log25"]:
            sweepmode = 3
        elif sweepmode in [4, "4", "LOG 50", "log 50", "LOG50", "log50"]:
            sweepmode = 4
        else:
            raise ValueError("Wrong input\n")

        if startval == None:
            startval = float(input("Enter start value: "))
        self.startval = startval

        if stopval == None:
            stopval = float(input("Enter stop value: "))
        self.stopval = stopval

        if sweepmode not in [2, 3, 4]:
            if stepval == None:
                stepval = float(input("Enter step value: "))
            self.stepval = stepval

        if compval == None:
            compval = float(input("Enter compliance value: "))
        self.compval = compval

        if sweepmode == 1:
            self._dev.write("SS {}{},{},{},{},{}".format(sourcemode, sweepmode, startval, stopval, stepval, compval))
        elif sweepmode in [2,3,4]:
            self._dev.write("SS {}{},{},{},{}".format(sourcemode, sweepmode, startval, stopval, compval))
        else:
            raise ValueError("Wrong input for sweepmode.\n")

    #===============================================================
    def _source_setup_var2(self, sourcemode = None, startval = None, stepval = None, nusteps = None, compval = None):
        """Set up VAR2.

        Input parameters
        ----------------
        (Setup for VAR1, VAR2, CONSTANT SMU): sourcemode: Source mode:
        Voltage Source: 1, "1", "v", "V"
        Current Source: 2, "2", "i", "I"

        (Setup for VAR1) sweepmode: sweep mode:
        1: LINEAR
        2: LOG 10
        3: LOG 25
        4: LOG 50

        (Setup for VAR1, VAR2) startval: start value

        (Setup for VAR1) stopval: stop value

        (Setup for VAR1, VAR2) stepval: step value

        (Setup for VAR2) nusteps: number of steps

        (Setup for VAR1, VAR2, CONSTANT SMU) compval: compliance value

        (Setup for CONSTANT SMU, CONSTANT Vs) outval: output value

        """
        if (self.sourcemode != None) and (self.sourcemode not in [3, "3", "com", "COM"]):
            self.sourcemode_ss = self.sourcemode
            sourcemode = self.sourcemode

        if sourcemode == None:
            sourcemode = input("Enter the source mode: ")
            self.sourcemode_ss = sourcemode
        if sourcemode in [1, "1", "v", "V"]:
            sourcemode = 'VP'
        elif sourcemode in [2, "2", "i", "I"]:
            sourcemode = 'IP'
        else:
            raise ValueError("Wrong input\n")

        if (self.sourcemode != None):
            if self.sourcemode in [1, "1", "v", "V"]:
                sourcemode_a = 'VP'
            elif self.sourcemode in [2, "2", "i", "I"]:
                sourcemode_a = 'IP'
            else:
                raise ValueError("Error\n")
            if (sourcemode != sourcemode_a):
                raise ValueError("Source mode defined in channel definition and source mode defined in source setup don't match.\n")

        if startval == None:
            startval = float(input("Enter start value: "))
        self.startval = startval

        if stepval == None:
            stepval = float(input("Enter step value: "))
        self.stepval = stepval

        if nusteps == None:
            nusteps = int(input("Enter number of steps: "))
        self.nusteps = nusteps

        if compval == None:
            compval = float(input("Enter compliance value: "))
        self.compval = compval

        self._dev.write("SS {} {},{},{},{}".format(sourcemode, startval, stepval, nusteps, compval))

    #===============================================================
    def _source_setup_const_smu(self, sourcemode = None, compval = None, outval = None):
        """Set up CONSTANT SMU.

        Input parameters
        ----------------
        (Setup for VAR1, VAR2, CONSTANT SMU): sourcemode: Source mode:
        Voltage Source: 1, "1", "v", "V"
        Current Source: 2, "2", "i", "I"

        (Setup for VAR1) sweepmode: sweep mode:
        1: LINEAR
        2: LOG 10
        3: LOG 25
        4: LOG 50

        (Setup for VAR1, VAR2) startval: start value

        (Setup for VAR1) stopval: stop value

        (Setup for VAR1, VAR2) stepval: step value

        (Setup for VAR2) nusteps: number of steps

        (Setup for VAR1, VAR2, CONSTANT SMU) compval: compliance value

        (Setup for CONSTANT SMU, CONSTANT Vs) outval: output value

        """
        if (self.sourcemode != None) and (self.sourcemode not in [3, "3", "com", "COM"]):
            self.sourcemode_ss = self.sourcemode
            sourcemode = self.sourcemode

        if sourcemode == None:
            sourcemode = input("Enter the source mode: ")
            self.sourcemode_ss = sourcemode
        if sourcemode in [1, "1", "v", "V"]:
            sourcemode = 'VC'
        elif sourcemode in [2, "2", "i", "I"]:
            sourcemode = 'IC'
        else:
            raise ValueError("Wrong input\n")

        if (self.sourcemode != None):
            if self.sourcemode in [1, "1", "v", "V"]:
                sourcemode_a = 'VC'
            elif self.sourcemode in [2, "2", "i", "I"]:
                sourcemode_a = 'IC'
            else:
                raise ValueError("Error\n")
            if (sourcemode != sourcemode_a):
                raise ValueError("Source mode defined in channel definition and source mode defined in source setup don't match.\n")

        if compval == None:
            compval = float(input("Enter compliance value: "))
        self.compval = compval

        if outval == None:
            outval = float(input("Enter output value: "))
        self.outval = outval

        self._dev.write("SS {}{},{:E},{}".format(sourcemode, self.channum, outval, compval))

    #===============================================================
    def _source_setup_const_vs(self, outval = None):
        """Set up CONSTANT Vs.

        Input parameters
        ----------------
        (Setup for VAR1, VAR2, CONSTANT SMU): sourcemode: Source mode:
        Voltage Source: 1, "1", "v", "V"
        Current Source: 2, "2", "i", "I"

        (Setup for VAR1) sweepmode: sweep mode:
        1: LINEAR
        2: LOG 10
        3: LOG 25
        4: LOG 50

        (Setup for VAR1, VAR2) startval: start value

        (Setup for VAR1) stopval: stop value

        (Setup for VAR1, VAR2) stepval: step value

        (Setup for VAR2) nusteps: number of steps

        (Setup for VAR1, VAR2, CONSTANT SMU) compval: compliance value

        (Setup for CONSTANT SMU, CONSTANT Vs) outval: output value

        """
        if outval == None:
            outval = float(input("Enter output value: "))
        self.outval = outval

        self._dev.write("SS SC{},{}".format(self.channum, outval))

    #===============================================================
    def _format_res(self, string = None):
        """Turn of a channel.

        Returns formated output.

        Input parameters
        ----------------
        string: output result

        """
        marker = None
        res = dict()
        lista = list()
        listn = list()
        listl = list()
        listv = list()
        listx = list()
        listc = list()
        listt = list()
        for s in string:
            if s in [",", "\r"]:
                lista = ''.join(lista)
                lista = lista.replace(' ', '')
                if marker == 'N':
                    listn.append(float(lista))
                elif marker == 'L':
                    listl.append(float(lista))
                elif marker == 'V':
                    listv.append(float(lista))
                elif marker == 'X':
                    listx.append(float(lista))
                elif marker == 'C':
                    listc.append(float(lista))
                elif marker == 'T':
                    listt.append(float(lista))
                else:
                    raise ValueError("Error\n")
                if s == "\r":
                    break
                marker = None
                lista = list()
            elif s == 'N':
                marker = 'N'
            elif s == 'L':
                marker = 'L'
            elif s == 'V':
                marker = 'V'
            elif s == 'X':
                marker = 'X'
            elif s == 'C':
                marker = 'C'
            elif s == 'T':
                marker = 'T'
            else:
                lista.append(str(s))

        res['N'] = listn
        res['L'] = listl
        res['V'] = listv
        res['X'] = listx
        res['C'] = listc
        res['T'] = listt

        if (len(res['L'])==0) and (len(res['V'])==0) and (len(res['X'])==0) and (len(res['C'])==0) and (len(res['T'])==0):
            res = listn

        return res
