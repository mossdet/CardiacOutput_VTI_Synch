"""
Obtain the shift in the Wearable timestamps with respect to Monitor data.
This is done by detecting the peaks in the smoothened Heart Rate data
from both devices and comparing the maximum peaks and their respective
timestamps. Timeshifts larger than 120 s lead to the maximum peak to be
ignored and the timeshift being calculated with the following Monitor peak down
the order.

Author: Daniel Lachner Piza
"""
# imports

import numpy as np

from get_state_change_idx import get_state_change_idx
from get_images_destination_path import get_images_destination_path
from dsp_tools import *


def get_peak_based_timeshift(mntr, wrbl, mov_avg_period_s):

    nf_fltr_sz = int(mntr['fs'] * mov_avg_period_s)
    fp_fltr_sz = int(mov_avg_period_s)

    stateChangeIdxs = get_state_change_idx(mntr)

    time_shifts_vec = []

    for stage in ['Baseline', 'Stage 1', 'Stage 2']:
        if stage == 'Baseline':
            selVecNF = slice(stateChangeIdxs[0], stateChangeIdxs[1])
            selVecFP = wrbl['stages'] == 'B'
        elif stage == 'Stage 1':
            selVecNF = slice(stateChangeIdxs[1], stateChangeIdxs[2])
            selVecFP = wrbl['stages'] == '1'
        elif stage == 'Stage 2':
            selVecNF = slice(stateChangeIdxs[2], stateChangeIdxs[3])
            selVecFP = wrbl['stages'] == '2'

        avgMetricVecNF = movmean(mntr['heartRate'][selVecNF], nf_fltr_sz)
        timeVecNF = mntr['time'][selVecNF]
        pksLocsNF = find_these_peaks(avgMetricVecNF)

        avgMetricVecFP = movmean(wrbl['heartRate'][selVecFP], fp_fltr_sz)
        timeVecFP = wrbl['time'][selVecFP] + timeVecNF[0]
        pksLocsFP = find_these_peaks(avgMetricVecFP)

        # Get max peak based time shift
        timeShift = 0
        fpPeakMaxLoc = pksLocsFP[0]
        fpPeakMaxTime = timeVecFP[fpPeakMaxLoc]
        for pi in range(len(pksLocsNF)):
            nfTempPeakMaxTime = timeVecNF[pksLocsNF[pi]]
            timeShift = nfTempPeakMaxTime - fpPeakMaxTime
            if abs(timeShift) < 120:
                break

        time_shifts_vec = np.append(time_shifts_vec, timeShift)
        wrbl['time'][selVecFP] = timeVecFP + timeShift

    return wrbl, time_shifts_vec
