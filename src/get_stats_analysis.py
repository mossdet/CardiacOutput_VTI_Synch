"""
For each paradigm stage, measure the Spearman correlation and linear regression R2 score between the CO rom Monitor and
both the VTI and estimated CO from Wearable.

Author: Daniel Lachner Piza
"""
# imports
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression

from get_state_change_idx import get_state_change_idx
from get_table_destination_path import get_table_destination_path
from dsp_tools import *


def get_stats_analysis_table(mntr, wrbl, mov_avg_period):

    epochDurS = 1

    stateChangeIdxs = get_state_change_idx(mntr)

    statsCell = [
        ['LBNP Stage', 'Monitor Metric', 'Wearable Metric', 'Spearman rho',
            'Spearman rho p value', 'Linear Regression R2', 'Nr.Observations']
    ]

    for fpMetricName in ['VTI', 'CO']:
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

            rho, pval, epochStartVec, epochsMonitor, epochsWearable = getStageStats(
                mntr, wrbl, selVecNF, selVecFP, mov_avg_period, epochDurS, fpMetricName)

            epochsMonitor = epochsMonitor.reshape(-1, 1)
            epochsWearable = epochsWearable.reshape(-1, 1)
            model = LinearRegression()
            model.fit(epochsWearable, epochsMonitor)
            rsqrd = model.score(epochsWearable, epochsMonitor)

            statsCell.append(
                [stage, 'CO', fpMetricName, rho, pval, rsqrd, len(epochsMonitor)])

    tableFN = get_table_destination_path() + 'Stats_Analysis_Table.csv'
    statsTable = pd.DataFrame(statsCell[1:], columns=statsCell[0])
    statsTable.to_csv(tableFN, index=False)


def getStageStats(mntr, wrbl, selVecNF, selVecFP, movAvgPeriodS, epochDurS, fpMetricName):
    nfFltrSz = mntr['fs'] * movAvgPeriodS
    fpFltrSz = movAvgPeriodS

    metricVecNF = mntr['cardiacOutput'][selVecNF]
    avgMetricVecNF = movmean(metricVecNF, nfFltrSz)
    timeVecNF = mntr['time'][selVecNF]

    if fpMetricName == 'VTI':
        metricVecFP = wrbl['vti'][selVecFP]
    else:
        metricVecFP = np.multiply(
            wrbl['vti'][selVecFP], wrbl['heartRate'][selVecFP])

    avgMetricVecFP = movmean(metricVecFP, fpFltrSz)
    timeVecFP = wrbl['time'][selVecFP]

    timeVecNF, avgMetricVecNF = remove_outliers(timeVecNF, avgMetricVecNF)
    timeVecFP, avgMetricVecFP = remove_outliers(timeVecFP, avgMetricVecFP)

    return getIntermetricCorrelation(avgMetricVecNF, timeVecNF, avgMetricVecFP, timeVecFP, epochDurS)


def getIntermetricCorrelation(metricVecNF, timeVecNF, metricVecFP, timeVecFP, epochDurS):
    discrtStart = max(timeVecNF[0], timeVecFP[0])
    discrtEnd = min(timeVecNF[-1], timeVecFP[-1])
    epochStartVec = np.arange(
        discrtStart, discrtEnd - epochDurS + 1, epochDurS)
    epochEndVec = np.arange(discrtStart + epochDurS, discrtEnd + 1, epochDurS)

    epochMat = np.column_stack((epochStartVec, epochEndVec))
    nrEpochs = len(epochMat)

    epochsMonitor = np.zeros(nrEpochs)
    epochsWearable = np.zeros(nrEpochs)

    for ei in range(nrEpochs):
        dataSelNF = np.logical_and(
            timeVecNF >= epochMat[ei, 0], timeVecNF <= epochMat[ei, 1])
        dataSelFP = np.logical_and(
            timeVecFP >= epochMat[ei, 0], timeVecFP <= epochMat[ei, 1])

        nfVal = 0
        if np.sum(dataSelNF) > 0:
            nfVal = np.mean(metricVecNF[dataSelNF])
        elif ei > 0:
            nfVal = epochsMonitor[ei - 1]
        else:
            print('no datapoints in this epoch-range')

        fpVal = 0
        if np.sum(dataSelFP) > 0:
            fpVal = np.mean(metricVecFP[dataSelFP])
        elif ei > 0:
            fpVal = epochsWearable[ei - 1]
        else:
            print('no datapoints in this epoch-range')

        epochsMonitor[ei] = nfVal
        epochsWearable[ei] = fpVal

    delSel = np.isnan(epochsMonitor) | np.isnan(epochsWearable)
    epochsMonitor = epochsMonitor[~delSel]
    epochsWearable = epochsWearable[~delSel]
    epochStartVec = epochStartVec[~delSel]

    rho, pval = spearmanr(epochsMonitor, epochsWearable)

    return rho, pval, epochStartVec, epochsMonitor, epochsWearable
