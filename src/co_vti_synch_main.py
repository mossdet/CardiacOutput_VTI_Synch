"""
Author: Daniel Lachner Piza
"""
# imports
import os
from get_datasets import get_datasets
from correct_wearable_timestamps import correct_wearable_timestamps
from get_state_change_idx import get_state_change_idx
from plot_paradigm_stages import plot_paradigm_stages
from plot_explorative_peaks import plot_explorative_peaks
from get_peak_based_timeshift import get_peak_based_timeshift
from plot_synchronized_metrics import plot_synchronized_metrics
from plot_stats_analysis import plot_stats_analysis
from get_stats_analysis import get_stats_analysis_table

# Start of workflow
# 1. Read the Datasets
path = os.path.dirname(os.path.abspath(__file__))
cutIdx = path.rfind(os.path.sep)
workspacePath = path[:cutIdx]
datasets_path = workspacePath + os.path.sep + 'Data' + os.path.sep

monitor_datapath = datasets_path + "labchartdata.csv"
wearable_datapath = datasets_path + "WearableData.xls"
[mntr, wrbl] = get_datasets(monitor_datapath, wearable_datapath)


# 2. Correct timestamp values that are lower than their following sample
wrbl = correct_wearable_timestamps(wrbl)


# 3. This function is used in the next steps, it defines the stages of the
# LBNP protocol for the Monitor data. It is called here only to display its use
state_change_idxs = get_state_change_idx(mntr)
plot_paradigm_stages(mntr)


# 4. All data is smoothened using a 10 second moving average
mov_avg_period = 10


# 5. Display the smoothened signals and the approach taken to correct the
# shift in the Wearable timestamps
plot_explorative_peaks(mntr, wrbl, mov_avg_period)

# 6. Obtain the shift in the Wearable timestamps with respect to Monitor data.
# This is done by detecting the peaks in the smoothened Heart Rate data
# from both devices and comparing the maximum peaks and their respective
# timestamps. Timeshifts larger than 120 s lead to the maximum peak to be
# ignored and the timeshift being calculated with the following peak down
# the order.
fpCorrected, time_shifts_vec = get_peak_based_timeshift(
    mntr, wrbl, mov_avg_period)


# 7. Plot the synchronized signals from Monitor and Wearable
plot_synchronized_metrics(mntr, fpCorrected, mov_avg_period, time_shifts_vec)

# 8. Plot the Spearman correlation and linear regression analysis between Monitor's Cardiac Output metric
# and the Wearable VTI metric
plot_stats_analysis(mntr, fpCorrected, mov_avg_period)

# 9. Save the results from the analysis of correlation to a table
get_stats_analysis_table(mntr, fpCorrected, mov_avg_period)
