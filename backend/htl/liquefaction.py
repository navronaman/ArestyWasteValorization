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
warnings.filterwarnings("ignore") # ignore warnings

# Fuel unit conversion
# https://h2tools.org/hyarc/calculator-tools/lower-and-higher-heating-values-fuels

from chaospy import distributions as shape
from exposan.htl import create_model

STATE_DATA = pd.read_csv("backend\\htl\\sludge_data_dmt.csv")

def htl_calc(kg_hr, mmbtu_to_gal=0.12845, kg_to_lb=2.20462):
    """
    Take the existing dry metric tonnes of sludge and return the minimum diesel selling price and global warming potential of diesel.
    
    Parameters
    ----------
    kg_hr : float
        Sludge in kg/hr.
    mmbtu_to_gal : float, optional
        Conversion factor for MMBTU to gal diesel. Default is 0.12845.
        1 MMBTU = 0.12845 gal diesel.
    kg_to_lb : float, optional
        Conversion factor for kg to lb. Default is 2.20462.
        1 kg CO2 = 2.20462 lb CO2.
        
    Returns
    -------
    MDSP : float
        Minimum diesel selling price in $/gal diesel.
    GWP : float
        Global warming potential of diesel in lb CO2/gal diesel.
        
    Raises
    ------
    TypeError
        If kg_hr is not a float.
    TypeError
        If mmbtu_to_gal is not a float.
    TypeError
        If kg_to_lb is not a float.
    
        
    Example
    -------
    htl_calc(15772549)
    >>> (2.5, 10)
    
    Notes
    -----
    1. If used in other parts, make sure to convert the sludge to kg/hr.
    2. The MSDP is in $/gal diesel, which can be converted to various other units.
    3. The GWP is in lb CO2/gal diesel, which can be converted to various other units.
    """
    
    # Raise errors if the input is not a float
    if not isinstance(kg_hr, (int, float)): # Type check
        raise TypeError("Sludge should be a float.")
    if not isinstance(mmbtu_to_gal, (int, float)): # Type check
        raise TypeError("MMBTU to gal should be a float.")
    if not isinstance(kg_to_lb, (int, float)): # Type check
        raise TypeError("KG to lb should be a float.")
    
    model = create_model(
        plant_size=True,
        feedstock='sludge',
        include_CFs_as_metrics=False,
        include_other_metrics=False,
        include_other_CFs_as_metrics=False,
    )
    
    param = model.parameter
    sys = model.system
    stream = sys.flowsheet.stream
    
    raw_wastewater = stream.feedstock_assumed_in_wastewater
    dist = shape.Uniform(12618039,18927059)
    
    @param(name='plant_size',
            element=raw_wastewater,
            kind='coupled',
            units='kg/hr',
            baseline=15772549,
            distribution=dist)
    
    def set_plant_size(i):
        raw_wastewater.F_mass=i
    plant_size = model.parameters[-1]
    
    for p in model.parameters:
        if p.name == 'Ww 2 dry sludge': break
    ww_2_dry_sludge = p.baseline # metric tonne/d/MGD (million gallon per day)
    
    print(f"WW 2 dry sludge: {ww_2_dry_sludge}")
    
    # Most important part of code
    plant_size.baseline = kg_hr
    
    df = model.metrics_at_baseline()
    
    # Want MDSP (minimum diesel selling price) and GWP diesel (global warming potential of diesel)
    MSDP, GWP = [m for m in model.metrics if m.name in ('MDSP', 'GWP diesel')]
    # MDSP is in $/gal diesel, GWP is in kg CO2/MMBTU diesel
    
    # Return the MSDP as it is, return GWP in lb CO2/gal diesel    
    return MSDP.get(), GWP.get()*mmbtu_to_gal*kg_to_lb

def htl_county(county, state_data=STATE_DATA):
    """
    Take a county name in New Jersey from the user and return the price and GWP.
    
    Parameters
    ----------
    name : str
        The name of the county.
        Available name - Atlantic, Bergen, Burlington, Camden, Cape May, Cumberland, Essex, Gloucester, Hudson, Hunterdon, Mercer, Middlesex, Monmouth, Morris, Ocean, Passaic, Salem, Somerset, Sussex, Union, Warren.
    state_data : pd.DataFrame, optional
        The data of the counties. Default is STATE_DATA.
        
    Returns
    -------
    name_final : str
        The name of the county.
    sludge : float
        The dry metric tonnes of sludge in that county.
    price : float
        The minimum diesel selling price in $/gal diesel.
    gwp : float
        The global warming potential of diesel in lb CO2/gal diesel.
        
    Raises
    ------
    ValueError
        If the county is not found.
    TypeError
        If the county is not a string.
    TypeError
        If the state_data is not a DataFrame.
    """
    
    if not isinstance(county, str): # Type check
        raise TypeError("County should be a string.")
    if not isinstance(state_data, pd.DataFrame): # Type check
        raise TypeError("State data should be a DataFrame.")    
    
    name_final = None
    for item in state_data["County"]:
        if county.lower() in item.lower():
            name_final = item
            break
    
    # Replaces the name with the final name from the dataset

    if name_final is None: # Value Check
        raise ValueError(f"County {county} not found.")
    
    mass_dmt = float(state_data.loc[state_data["County"] == name_final, "County Total (Dry Metric Tonnes/Year)"].values[0])

    # Let's convert dry metric tonnes to kg/hr
    mass_kg_hr = mass_dmt * 1000 / 24 # 24 hours in a day
    
    # Let's get the MSDP and GWP
    msdp, gwp = htl_calc(mass_kg_hr)
    
    return name_final, mass_dmt, msdp, gwp

# Let's write some test cases
if __name__ == "__main__":
    # Test 1
    print(htl_calc(150)) # (397878.8243590509, 408526.3837657836)
    
    # Test 2
    try:
        print(htl_calc("150")) # Expected: TypeError
    except TypeError as e:
        print(e)
    
    # Test 2
    print(htl_county("Atlantic")) # Expected: ('Atlantic', 8991.7, 162.62884976030858, 176.06916214025898)
    
    # Test 3
    try:
        print(htl_county("XYZ")) # Expected: ValueError
    except ValueError as e:
        print(e)
    
    # Test 4
    try:
        print(htl_county(123)) # Expected: TypeError
    except TypeError as e:
        print(e)
    
    # Test 5
    try:
        print(htl_county("Atlantic", "XYZ")) # Expected: TypeError
    except TypeError as e:
        print(e)