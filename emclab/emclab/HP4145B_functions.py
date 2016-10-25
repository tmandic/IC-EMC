from .HP4145B import HP4145B

def open_channels(list_of_params):
    # turn off all channels
    params = list_of_params[0]
    hp = HP4145B(**params)
    hp.start()
    for i in range(1, 5):
        hp.turn_off_chan(cd = 'smu', channum = i)
        if i in [1,2]:
            hp.turn_off_chan(cd = 'vs', channum = i)
            hp.turn_off_chan(cd = 'vm', channum = i)

    # define all channels
    hps = list()
    for params in list_of_params:
        hp = HP4145B(**params)
        hps.append(hp)

    return hps

def source_setup(list_of_hps, list_of_params):
    # set up all channels
    for hp, params_hp in zip(list_of_hps, list_of_params):
        hp.source_setup(**params_hp)

def list_setup(list_of_hps):
    hp0 = list_of_hps[0]
    sent = "SM DM2 LI "
    lista = list()
    for hp in list_of_hps:
        if hp.cd not in ['VS', 'Vs', 'vs', '2', 2]:
            comma = ','
            if hp == list_of_hps[-1]:
                comma = ''
            if hp.sourcemode_ss in [1, "1", "v", "V"]:
                sent = sent + "'" + hp.iname + "'" + comma
                lista.append(hp.iname)
            elif hp.sourcemode_ss in [2, "2", "i", "I"]:
                sent = sent + "'" + hp.vname + "'" + comma
                lista.append(hp.vname)
            else:
                raise ValueError("Wrong input\n")

    hp0._dev.write(str(sent))
    print("Monitor channels:\n{}".format(str(lista).replace('[', '').replace(']', '')))

def meas_setup(list_of_hps, interval = None, nureadings = None, wait = None):
    if wait == None:
        wait = 0
    if interval == None:
        interval = float(input("Measurement interval: "))
    if nureadings == None:
        nureadings = int(input("Number of readings: "))
    list_of_hps[0]._dev.write("SM WT {}".format(wait))
    list_of_hps[0]._dev.write("SM IN {}".format(interval))
    list_of_hps[0]._dev.write("SM NR {}".format(nureadings))
    for hp in list_of_hps:
        hp.wait = wait
        hp.interval = interval
        hp.nureadings = nureadings
    print("Measurement has been set up with the following settings:")
    print("Wait time: {} s\nInterval time: {} s\nNumber of readings: {}\n".format(wait, interval, nureadings))

def measure(list_of_hps, mode, osc = None, osc1 = None, osc2 = None):
    hp0 = list_of_hps[0]
    hp0.measure(mode = mode, osc = osc, osc1 = osc1, osc2 = osc2)
    meas = dict()
    for hp in list_of_hps:
        if hp.cd not in ['VS', 'Vs', 'vs', '2', 2]:
            meas[hp.param] = hp.get_res()
    print(meas)
    return meas
