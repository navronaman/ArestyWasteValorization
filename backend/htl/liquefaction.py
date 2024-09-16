"""
What does this file do?

It created two important functions that will be called throughout the project:
1. htl_calc: This function calculates the minimum diesel selling price (MDSP) and the global warming potential of diesel (GWP) based on the dry metric tonnes of sludge.
2. htl_county: This function takes a county name of New Jersey from the user and returns the price and GWP of diesel for that county.

Where is this file used in the project?
1. dmt_report.py - These functions generate a final csv file for the HTL findings
2. app.py - These functions are called on the flask server

What does this file rely on?
1. dmt_dataextract.py - This file is used to extract data from the pdf, which is called by htl_county
2. exposan.htl - Called by importing
3. warnings, pandas, chaospy - Imported libraries
"""

import warnings
import pandas as pd
warnings.filterwarnings("ignore")

def htl_calc():
    pass

def htl_county():
    pass