# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class HP4145B(GPIB):
    """Semiconductor Parameter Analyzer HP/Agilent 4145B.

    """
    #===============================================================
    def __init__(self, addr, cd = None, channum = None,
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

        # get instrument name
        self.name = self._name()

        self.start()

        self.chan_def(cd, channum, vname, sourcefunction, iname, sourcemode)

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

        print("Channel {} - {} defined with the following parameters:\nVoltage name: {}".format(cd_a, self.channum, self.vname))

        if self.iname != None:
            print("Current name: {}".format(self.iname))

        if self.sourcemode != None:
            if self.sourcemode in [1, "1", "v", "V"]:
                sourcemode = "1: V"
            elif self.sourcemode in [2, "2", "i", "I"]:
                sourcemode = "2: I"
            elif self.sourcemode in [3, "3", "com", "COM"]:
                sourcemode = "3: COM"
            else:
                raise ValueError("Wrong input\n")
            print("Source mode: {}".format(sourcemode))

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
            print("Source function: {}\n".format(sourcefunction))

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
            sf = "VAR3"
            if self.cd in ['SMU', 'smu', "1", 1]:
                self._source_setup_const_smu(sourcemode = sourcemode, compval = compval, outval = outval)
            elif self.cd in ['VS', 'Vs', 'vs', "2", 2]:
                self._source_setup_const_vs(outval = outval)
            else:
                raise ValueError("Error")
        else:
            raise ValueError("Error")

        print("Source {} is set up with the following parameters:".format(sf))

        if self.sourcemode_ss != None:
            if self.sourcemode_ss in [1, "1", "v", "V"]:
                sourcemode = '1: V'
            elif self.sourcemode_ss in [2, "2", "i", "I"]:
                sourcemode = '2: I'
            else:
                raise ValueError("Wrong input\n")
            print("Source mode is: {}".format(sourcemode))

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
            print("Sweep mode: {}".format(sweepmode))

        if self.startval != None:
            print("Start value: {}".format(self.startval))

        if self.stopval != None:
            print("Stop value: {}".format(self.stopval))

        if self.stepval != None:
            print("Step value: {}".format(self.stepval))

        if self.nusteps != None:
            print("Number of steps: {}".format(self.nusteps))

        if self.outval != None:
            print("Output value: {}".format(self.outval))

        if self.compval != None:
            print("Compliance value: {}".format(self.compval))

    #===============================================================
    def measure(self, me = None, param = None):
        """Set the integration time.

        Returns output.

        Input parameters
        ----------------
        me: measure mode:
        1 - SINGLE
        2 - REPEAT
        3 - APPEND
        4 - STOP

        param: parameter name you want to measure:
        voltage name or current name (if available)

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

        if param == None:
            if self.iname == None:
                param = self.vname
            elif self.iname != None:
                param = input("Type in one of the channel names you want to measure:\n 1 - {} or 2 - {}\n".format(self.vname, self.iname))
            else:
                raise ValueError("Error\n")

        if param in [1, '1', self.vname]:
            param = self.vname
        elif param in [2, '2', self.iname]:
            if self.iname == None:
                raise ValueError("The current name is None\n")
            param = self.iname
        else:
            raise ValueError("Wrong input.\n")


        print("Measuring of {} started in mode: {}\n".format(param, me_a))

        output = self._dev.query("MD ME{}\r\n".format(me))

        A = self._dev.query("SPOLL({})\r\n".format(output))
        while self._dev.query("BIT ({},0)\r\n".format(A)) == 0:
            A = self._dev.query("SPOLL({})\r\n".format(output))

        output = self._dev.query("DO '{}'\r\n".format(param))

        return output

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
            self._dev.write("DE CH{}\r\n".format(channum))
        elif cd in ['VS', 'Vs', 'vs', '2', 2]:
            self._dev.write("DE VS{}\r\n".format(channum))
        elif cd in ['VM', 'Vm', 'vm', '3', 3]:
            self._dev.write("DE VM{}\r\n".format(channum))
        else:
            raise ValueError("Wrong input.\n")

        print("Channel {}-{} turned of.\n".format(cd, channum))

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
        self.integration_time(it = it)
        time.sleep(1)
        self.calibration(ca = ca)
        time.sleep(1)
        self.data_ready(dr = dr)
        time.sleep(1)
        self.buffer_clear()
        time.sleep(1)

        print("Started the device.\n")

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

        self._dev.write("IT{}\r\n".format(it))
        print("Integration time has been set to mode: {}\n".format(it_a))

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

        self._dev.write("CA{}\r\n".format(ca))
        print("Auto calibration is {}\n".format(ca_a))

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

        self._dev.write("DR{}\r\n".format(dr))

    #===============================================================
    def buffer_clear(self):
        """Clears the data output buffer.

        """
        self._dev.write("BC\r\n")
        print("Data output buffer cleared.\n")

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

        print("DE CH{},'{}','{}',{},{}\r\n".format(channum, self.vname, self.iname, sourcemode, sourcefunction))

        self._dev.write("DE CH{},'{}','{}',{},{}\r\n".format(channum, self.vname, self.iname, sourcemode, sourcefunction))

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
        print(sourcefunction)
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

        print("DE VS{},'{}',{}\r\n".format(channum, self.vname, sourcefunction))

        self._dev.write("DE VS{},'{}',{}\r\n".format(channum, self.vname, sourcefunction))

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

        print("DE VM{},'{}'\r\n".format(channum, self.vname))

        self._dev.write("DE VM{},'{}'\r\n".format(channum, self.vname))

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
            print("SS {}{},{},{},{},{}\r\n".format(sourcemode, sweepmode, startval, stopval, stepval, compval))
            self._dev.write("SS {}{},{},{},{},{}\r\n".format(sourcemode, sweepmode, startval, stopval, stepval, compval))
        elif sweepmode in [2,3,4]:
            print("SS {}{},{},{},{}\r\n".format(sourcemode, sweepmode, startval, stopval, compval))
            self._dev.write("SS {}{},{},{},{}\r\n".format(sourcemode, sweepmode, startval, stopval, compval))
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

        print("SS {} {},{},{},{}\r\n".format(sourcemode, startval, stepval, nusteps, compval))
        self._dev.write("SS {} {},{},{},{}\r\n".format(sourcemode, startval, stepval, nusteps, compval))

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

        print("SS {}{},{},{}\r\n".format(sourcemode, self.channum, outval, compval))
        self._dev.write("SS {}{},{},{}\r\n".format(sourcemode, self.channum, outval, compval))

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

        print(("SS SC{},{}\r\n".format(self.channum, outval)))
        self._dev.write("SS SC{},{}\r\n".format(self.channum, outval))

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
