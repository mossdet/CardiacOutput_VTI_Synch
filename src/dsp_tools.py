"""
Implemenet DSP methods

Author: Daniel Lachner Piza
"""
# imports
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import uniform_filter1d
from scipy.stats import iqr


def find_these_peaks(signal_vec):
    # return peak locations sorted in descending order
    peaksLocs = find_peaks(signal_vec, distance=3, prominence=3)[0]
    peaksLocs = peaksLocs[np.argsort(signal_vec[peaksLocs])]
    peaksLocs = peaksLocs[::-1]
    return peaksLocs


# Symmetric moving average filter
def movmean(signal, windowSize):
    # window = np.ones(windowSize) / windowSize
    # movAvg = np.convolve(signal, window, mode='same')
    movAvgSig = uniform_filter1d(signal, size=windowSize)
    return movAvgSig


# Remove outliers based on the inter-quartile range
def remove_outliers(time, signal):
    iqrVal = iqr(signal)
    medianVal = np.median(signal)
    # stdVal = np.std(signal)
    th = 2.5
    lowLim = medianVal - th*iqrVal
    highLim = medianVal + th*iqrVal
    delVec = (signal < lowLim) | (signal > highLim)
    time = np.delete(time, delVec)
    signal = np.delete(signal, delVec)

    return time, signal
