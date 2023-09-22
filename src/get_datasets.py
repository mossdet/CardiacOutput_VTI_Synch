"""
Read the datasets

Author: Daniel Lachner Piza
"""

import numpy as np
import pandas as pd

#########################################################
# Load Monitor and Wearable datasets


def get_datasets(monitor_datapath, wearable_datapath):

    # Load Monitor data
    mntrTable = pd.read_csv(monitor_datapath)
    mntr = {
        'time': np.array(mntrTable['TimeSec']),
        'pressChamb': np.array(mntrTable['PressureChamber']),
        'heartRate': np.array(mntrTable['HR']),
        'cardiacOutput': np.array(mntrTable['CO']),
        'fs': 1000,
        'nSamples': len(mntrTable)
    }

    # Load Wearable data
    wrblTable = pd.read_excel(wearable_datapath)
    x = 1
    wrbl = {
        'stages': np.array(wrblTable['Stage']),
        'time': np.array(wrblTable['Time (s)']),
        'heartRate': np.array(wrblTable['HR']),
        'ccft': np.array(wrblTable['cCFT']),
        'vti': np.array(wrblTable['Vmax VTI Total']),
        'psv': np.array(wrblTable['PSV'])
    }

    return mntr, wrbl
