"""
For the Monitor dataset, get the sample indices that represent a new stage in the LBNP paradigm.
The average pressure for each stage corresponds to the average pressure between minutes 2.5 and 3.5
As soon as a sample is below this average, a new stage is detected

Author: Daniel Lachner Piza
"""
# imports
import numpy as np


def get_state_change_idx(mntr):
    # Get indexes for state changes based on LBNP
    # Get average Pressure for each state based on the stage period (5 min)
    states_avg_p = []
    for si in range(int(2.5 * 60 * mntr['fs']), mntr['nSamples'], int(5 * 60 * mntr['fs'])):
        state_avg_p = np.mean(mntr['pressChamb'][si:si + int(60 * mntr['fs'])])
        states_avg_p.append(state_avg_p)

    # Get index of state changes based on comparing pressure from current and next stage
    state_change_idxs = [0]
    for spi in range(len(states_avg_p) - 1):
        spA = states_avg_p[spi]
        spB = states_avg_p[spi + 1]
        spMid = np.mean([spA, spB])

        schi = np.argmax(mntr['pressChamb'] < spMid)
        if schi < state_change_idxs[-1]:
            schi = np.argmax((mntr['pressChamb'] > spMid) &
                             (mntr['time'] > mntr['time'][state_change_idxs[-1]]))

        state_change_idxs.append(schi)

    return state_change_idxs
