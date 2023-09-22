"""
For each paradigm stage, measure the Spearman correlation and linear regression R2 score between the CO rom Monitor and
both the VTI and estimated CO from Wearable (HR*VTI).

Author: Daniel Lachner Piza
"""
# imports
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from get_state_change_idx import get_state_change_idx
from get_images_destination_path import get_images_destination_path
from get_stats_analysis import getStageStats


def plot_stats_analysis(mntr, wrbl, mov_avg_period):

    epochDurS = 1

    stateChangeIdxs = get_state_change_idx(mntr)

    metricIdx = 4
    for fpMetricName in ['VTI', 'CO']:

        fig, axs = plt.subplots(2, 3, figsize=(16, 9))
        fig.suptitle(
            'Monitor CO vs. Wearable' + fpMetricName + '\n' + 'Spearman Correlation and Linear Regression Analysis')

        colIdx = 0
        left_color = [0, 0.45, 0.74]
        right_color = [0.93, 0.7, 0.13]

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
            regY = model.predict(epochsWearable)
            rsqrd = model.score(epochsWearable, epochsMonitor)

            # Correlation
            ax1 = axs[0, colIdx]
            ax1.set_title(stage + "\n"
                          f"Spearman's rank rho: {rho:.2f} (p < {pval:.2e})")

            ax1.plot(epochStartVec, epochsMonitor, '-',
                     color=left_color, linewidth=2)
            ax1.set_ylim(min(epochsMonitor), max(epochsMonitor))
            ax1.set_xlim(min(epochStartVec), max(epochStartVec))
            ax1.set_ylabel("Monitor Cardiac Output")
            ax1.set_xlabel("Time (s)")
            ax1.legend(["Monitor Cardiac Output"], loc='upper left')

            ax2 = ax1.twinx()
            ax2.plot(epochStartVec, epochsWearable, '-',
                     color=right_color, linewidth=2)
            ax2.set_ylim(min(epochsWearable), max(epochsWearable))
            ax2.set_xlim(min(epochStartVec), max(epochStartVec))
            ax2.set_ylabel("Wearable" + fpMetricName)
            ax2.set_xlabel("Time (s)")
            ax2.legend(["Wearable " + fpMetricName], loc='upper right')

            # Regression
            ax1 = axs[1, colIdx]
            ax1.set_title(stage + "\n"
                          f"Linear Regression $R^2$: {rsqrd:.2f}")

            ax1 = axs[1, colIdx]
            ax1.plot(epochsWearable, epochsMonitor, 'ob', linewidth=0.5)
            ax1.plot(epochsWearable, regY, '-k', linewidth=1)
            ax1.set_ylim(min(epochsMonitor), max(epochsMonitor))
            ax1.set_ylabel("Monitor Cardiac Output")
            ax1.set_xlabel("Wearable " + fpMetricName)

            colIdx += 1

        plt.tight_layout()

        figFilename = get_images_destination_path(
        ) + f"{metricIdx}" + "_Monitor_CO_vs_Wearable_" + fpMetricName + ".png"
        plt.savefig(figFilename, bbox_inches='tight', dpi=150)
        metricIdx += 1
