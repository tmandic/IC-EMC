from .HP4145B import HP4145B

def open_channels(list_of_params):
    # turn off all channels
    params = list_of_params[0]
    hp = HP4145B(**params)
    for i in range(1, 5):
        hp.turn_off_chan(cd = 'smu', channum = i)
    for i in range(1, 3):
        hp.turn_off_chan(cd = 'vs', channum = i)
    for i in range(1, 3):
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
