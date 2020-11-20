import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import butter, lfilter
from sklearn.preprocessing import normalize
from sklearn.neighbors import KNeighborsClassifier

def bandfilter(ax, ay, az):
    b, a = butter(3, [0.5, 20], 'bandpass', fs=50)
    ax_f, ay_f, az_f = lfilter(b, a, ax) , lfilter(b, a, ay), lfilter(b, a, az)
    return ax_f, ay_f, az_f

def get_peaks(az, time_scale, time_millis, distance=600):
    az_mean = np.mean(az)
    peaks,_ = find_peaks(az, distance= distance/time_scale, height = az_mean + 10)
    print(f"peaks indices = {peaks}")
    print(f"peaks values = { [ round(az[peak],2) for peak in peaks ]}")
    return peaks

def generate_windows(dims, time_scale, time_millis, peaks, num_readings=40):
    print(f"window time = {num_readings * time_scale}ms")
    # windows store the az readings for various windows
    windows = []
    window_times = []
    for peak in peaks:
        window, window_time = [], []
        # include half of the readings on either side of the peak
        lower = int(peak - num_readings/2)
        upper = int(peak + num_readings/2)
        # skip windows that are out of bounds
        if lower < 0 or upper >= len(dims[0]):
            print(f"peak at t={time_millis[peak]} has an out of bounds window")
            continue
        # each window is of the format [ ax0, ay0, az0, ax1, ay1, az1, ... , axn, ayn, azn ]
        # consisting of n readings centred around the strike point in the z-axis
        for i in range(lower, upper):
            curr = []
            for dim in dims:
                curr.append(round(dim[i],3))
            window.extend(curr)
            window_time.append(time_millis[i])
        windows.append(window)
        window_times.append(window_time)
    return windows, window_times

#################################################
# Main classification function ##################
#################################################
# Returns None if test data is insufficient     #
# Returns True if the test data belongs to Otto #
# Returns False is the test data belongs to Has #
#################################################

def classify(test_ax, test_ay, test_az):

    assert(len(test_ax) == len(test_ay) == len(test_az))
    
    time_millis = [ i*20 for i in range(0, len(test_ax)) ]
    
    #X_train = np.load('X_train.npy')
    #y_train = np.load('y_train.npy')
    print("Training...")
    clf = KNeighborsClassifier(n_neighbors=4)
    clf.fit(X_train, y_train)
    
    print("Processing test data")
    # time_scale is the no. of milliseconds between readings
    time_scale = 20
    # apply bandpass filter to training data    
    test_ax_f, test_ay_f, test_az_f = bandfilter(test_ax, test_ay, test_az)
    # get peaks
    peaks = get_peaks(test_ay_f, time_scale, time_millis, distance=600)
    # generate windows
    X_test, _ = generate_windows([test_ax_f, test_ay_f, test_az_f], time_scale, time_millis, peaks, num_readings=20)
    if len(X_test) == 0:
        print(f"Test data insufficient - only {len(peaks)} peaks detected.")
        return None
    res = list(clf.predict(X_test))
    print(f"U1 count = {res.count('u1')}")
    print(f"U2 count = {res.count('u2')}")
    return res.count('u1') > res.count('u2')