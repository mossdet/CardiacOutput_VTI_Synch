"""
Correct Wearable timestamps that go back in time
Whenever such a timestampis found, replace it by the previous timestamp plus the average time step

Author: Daniel Lachner Piza
"""
# imports
import numpy as np
import matplotlib.pyplot as plt


def correct_wearable_timestamps(wrbl):

    corrTimeStage = wrbl['time'][wrbl['stages'] == 'B']
    avgTimestep = np.mean(np.diff(corrTimeStage))
    for ti in range(0, len(corrTimeStage)-1):
        if corrTimeStage[ti + 1] - corrTimeStage[ti] <= 0:
            corrTimeStage[ti + 1] = corrTimeStage[ti] + avgTimestep
    wrbl['time'][wrbl['stages'] == 'B'] = corrTimeStage

    corrTimeStage = wrbl['time'][wrbl['stages'] == '1']
    avgTimestep = np.mean(np.diff(corrTimeStage))
    for ti in range(len(corrTimeStage)-1):
        if corrTimeStage[ti + 1] - corrTimeStage[ti] <= 0:
            corrTimeStage[ti + 1] = corrTimeStage[ti] + avgTimestep
    wrbl['time'][wrbl['stages'] == '1'] = corrTimeStage

    corrTimeStage = wrbl['time'][wrbl['stages'] == '2']
    avgTimestep = np.mean(np.diff(corrTimeStage))
    for ti in range(len(corrTimeStage) - 1):
        if corrTimeStage[ti + 1] - corrTimeStage[ti] <= 0:
            corrTimeStage[ti + 1] = corrTimeStage[ti] + avgTimestep
    wrbl['time'][wrbl['stages'] == '2'] = corrTimeStage

    # pp.plot(wrbl['time'])
    # pp.show()
    return wrbl
