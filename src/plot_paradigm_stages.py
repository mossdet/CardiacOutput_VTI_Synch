"""
Plot estimated paradigm stages

Author: Daniel Lachner Piza
"""

import matplotlib.pyplot as plt

from get_state_change_idx import get_state_change_idx
from get_images_destination_path import get_images_destination_path


def plot_paradigm_stages(mntr):
    state_change_idxs = get_state_change_idx(mntr)

    plt.figure('Paradigm Stages')

    plt.plot(mntr['time'], mntr['pressChamb'], '-k', linewidth=0.5)
    for i in range(len(state_change_idxs)-1):
        plt.plot([mntr['time'][state_change_idxs[i]], mntr['time'][state_change_idxs[i]+1]],
                 [min(mntr['pressChamb']), max(mntr['pressChamb'])], '-r')

    plt.xlim([min(mntr['time']), max(mntr['time'])])
    plt.ylim([min(mntr['pressChamb']), max(mntr['pressChamb'])])

    plt.title('LBNP Pressure')
    plt.xlabel('Time (s)')
    plt.ylabel('LBNP (mmHg)')

    plt.gca().set_position([0, 0, 1, 1])
    plt.gca().set_facecolor((1, 1, 1))

    figFilename = get_images_destination_path() + '1_Paradigm_Stages.png'
    plt.savefig(figFilename, bbox_inches='tight', dpi=150)
