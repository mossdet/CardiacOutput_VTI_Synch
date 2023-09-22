"""
Plot the synchronized hear rate signals from Monitor and Wearable.

Author: Daniel Lachner Piza
"""
# imports
import matplotlib.pyplot as plt
from dsp_tools import *

from get_state_change_idx import get_state_change_idx
from get_images_destination_path import get_images_destination_path


def plot_synchronized_metrics(mntr, wrbl, mov_avg_period_s, time_shifts_vec):

    nf_fltr_sz = int(mntr['fs'] * mov_avg_period_s)
    fp_fltr_sz = int(mov_avg_period_s)

    stateChangeIdxs = get_state_change_idx(mntr)

    fig, axs = plt.subplots(2, 3, figsize=(16, 9))

    fig.suptitle(
        'Corrected Wearable Timestamps \n (Max Peaks based correction)')

    colIdx = 0
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

        metricVecNF = mntr['heartRate'][selVecNF]
        avgMetricVecNF = movmean(metricVecNF, nf_fltr_sz)
        timeVecNF = mntr['time'][selVecNF]
        pksLocsNF = find_these_peaks(avgMetricVecNF)

        metricVecFP = wrbl['heartRate'][selVecFP]
        avgMetricVecFP = movmean(metricVecFP, fp_fltr_sz)
        timeVecFP = wrbl['time'][selVecFP]
        pksLocsFP = find_these_peaks(avgMetricVecFP)

        # Monitor
        ax1 = axs[0, colIdx]
        ax1.plot(timeVecNF, metricVecNF, '-',
                 color=[0.2, 0.5, 0.9, 0.5], linewidth=1.5)
        ax1.set_ylim(min(metricVecNF), max(metricVecNF))
        ax1.set_ylabel("Heart Rate (BPM)")
        ax1.set_title(stage + "\n Monitor Heart Rate")
        ax1.legend(["Monitor HR"], loc='upper right')
        ax2 = ax1.twinx()
        ax2.plot(timeVecNF, avgMetricVecNF, '-k', linewidth=1.5)
        ax2.plot(timeVecNF[pksLocsNF], avgMetricVecNF[pksLocsNF], 'or')
        ax2.set_ylim(min(avgMetricVecNF), max(avgMetricVecNF))
        ax2.set_ylabel("10s Avg Heart Rate (BPM)")
        ax2.set_xlim(min(timeVecNF), max(timeVecNF))
        ax2.set_xlabel('Time (s)')
        ax2.legend(["Monitor smooth HR"], loc='lower right')

        # Wearable
        ax1 = axs[1, colIdx]
        ax1.plot(timeVecFP, metricVecFP, '-',
                 color=[0.2, 0.5, 0.9, 0.5], linewidth=1.5)
        ax1.set_ylim(min(metricVecFP), max(metricVecFP))
        ax1.set_ylabel("Heart Rate (BPM)")
        ax1.set_title(
            f"Baseline \n Wearable Heart Rate \n Timeshift: {time_shifts_vec[colIdx]:.3f} s")
        ax1.legend(["Wearable HR"], loc='upper right')
        ax2 = ax1.twinx()
        ax2.plot(timeVecFP, avgMetricVecFP, '-k', linewidth=1.5)
        ax2.plot(timeVecFP[pksLocsFP], avgMetricVecFP[pksLocsFP], 'or')
        ax2.set_ylim(min(avgMetricVecFP), max(avgMetricVecFP))
        ax2.set_ylabel("10s Avg Heart Rate (BPM)")
        ax2.set_xlim(min(timeVecNF), max(timeVecNF))
        ax2.set_xlabel('Time (s)')
        ax2.legend(["Wearable smooth HR"], loc='lower right')

        colIdx += 1

    plt.tight_layout()
    figFilename = get_images_destination_path() + '3_Synchronized_Metrics.png'
    plt.savefig(figFilename, bbox_inches='tight', dpi=150)
