import pandas as pd
import numpy as np
import os

"""
problem is that mn and cin have different freqs 

so either we can find the freqs of the neurons, and pick 


"""

PATH = "data/"
files = [f'{PATH}{f}' for f in os.listdir(PATH) if f.endswith(".txt")]
# print(files, len(files))

def get_ts(fname):
    """
    get timeseries from text file
    preprocess the v (which I think is 0.1v, into mV)
    return the two column file as a numpy array of shape (-1, 2)
    """
    print(f"fetching {fname}")
    ts = np.loadtxt(fname)
    # preprocess, some contain mV, some contain V
    #TODO also ignore the time column, and make it from 0 at timestep of 0.1 ms
    # bring everything to mV?
    # the filename contains v, then it is in units of 0.1 volts (i think?)
    hasv = fname.split('_')[1][0] == 'v'
    if hasv:
        ts[:, 1] = ts[:, 1].copy()*100
    return ts

def get_frate(df):
    """
    spikes = zerocrossings?
    measure zerocrossings in dataframe 
    ! zerocrossings from below !
    """
    vtrace = df[:, 1]
    # print("vtrace shape", vtrace.shape)
    interval = df.shape[0] # resolution is 0.1 ms, so we divide by 0.1 * 0.001

    interval_sec = interval / 10000
    # print("interval (sec)", interval_sec)
    spiketimes = [] # to get the isi's

    nspikes = 0
    for t in range(1, df.shape[0]):
        if vtrace[t] > 0 and vtrace[t-1] < 0:
            spiketimes.append(t)
            nspikes += 1

    # print("n spikes", nspikes)

    
    frate = nspikes / (interval_sec)
    # print('firing rate : ', frate, " Hz")

    print(f"nspikes : {nspikes}, interval : {interval_sec}, frate = {frate}")

    # isi
    ISIs = np.diff(spiketimes)
    if nspikes > 2:
        cv = ISIs.std()/ISIs.mean()
        print("ISI CV = ", cv)
    else:
        print('too few spikes for finding cv!')


    print("\n\n")

    
    





for file in files:
    ts = get_ts(file)
    get_frate(ts)
