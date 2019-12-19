# -*- coding: utf-8 -*-
"""
File that reads in data
"""

import pandas as pd


def load_data():

    df = pd.read_csv("data_test.csv", sep=',', index_col=0, header=0)
    return df
