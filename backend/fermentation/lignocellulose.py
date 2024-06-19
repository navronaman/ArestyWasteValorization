#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan-webapp: Web application for QSDsan

This module is developed by:
    
    Yalin Li <mailto.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/main/LICENSE.txt
for license details.
'''

import biosteam as bst
from biorefineries.cellulosic import Biorefinery as CellulosicEthanol
from biorefineries.cellulosic.streams import cornstover as cornstover_kwargs
from biorefineries.cornstover import ethanol_density_kggal
import pandas as pd

GWP_CFs = {
    'cornstover': 0.2,
    'sulfuric_acid': 1,
    'ammonia': 1,
    'cellulase': 1, #!!! note water content
    'CSL': 1,
    'caustic': 1, #!!! note water content    
    'FGD_lime': 1, #!!! need to be clear if this is CaO or Ca(OH)2
    }

STATE_DATA = pd.read_csv(r'backend\fermentation\biomass_data.csv')
STATE_DATA["Kilogram"] = STATE_DATA["Lignocellulose (dry tons)"] * 907.185
STATE_DATA["Kilogram/hr"] = STATE_DATA["Kilogram"] / (365*24*0.96)


def calculate_annual_ethanol_price_GWP(mass, cornstover_price=0.2, GWP_CFs=GWP_CFs, characterization_factors=(1., 1.,), power_utility_price=0.07):
    """
    Calculate the annual ethanol price and GWP based on the given mass of ethanol produced.
    
    Parameters
    ----------
    mass : float
        The annual mass of ethanol produced (kg/yr).
    cornstover_price : float
        The price of cornstover (USD/kg).
        Set to default of 0.2
    GWP_CFs : dict
        Global warming potential characterization factors (kg CO2-eq/kg).
        Contains the following:
        - 'cornstover': price of cornstover (USD/kg) [0.2]
        - 'sulfuric_acid': price of sulfuric acid (USD/kg) [1]
        - 'ammonia': price of ammonia (USD/kg) [1]
        - 'cellulase': price of cellulase (USD/kg) [1]
        - 'CSL': price of CSL (USD/kg) [1]
        - 'caustic': price of caustic (USD/kg) [1]
        - 'FGD_lime': price of FGD lime (USD/kg) [1]
    characterization_factors : tuple
        Global warming potential characterization factors (kg CO2-eq/kg).
        Contains the following:
        - consumption
        - production
        Set to default value of (1., 1.).
    power_utility_price : float
        Price of power utility (USD/kWh).
        Set to default value of 0.07.
    """
    
    br = CellulosicEthanol(
        name='ethanol',
        )
    sys = br.sys
    tea = sys.TEA
    f = sys.flowsheet
    stream = f.stream
    feedstock = stream.cornstover
    ethanol = stream.ethanol
    
    feedstock.F_mass = mass 
    
    prices = {
        'cornstover': cornstover_price,
        }
    for ID, price in prices.items(): stream.search(ID).price = price
    bst.PowerUtility.price = power_utility_price
    
    for ID, CF in GWP_CFs.items(): stream.search(ID).characterization_factors['GWP'] = CF
    bst.PowerUtility.characterization_factors['GWP'] = characterization_factors
    
    sys.simulate()
    
    get_ethanol = lambda: ethanol.F_mass*ethanol_density_kggal*tea.operating_hours/1e6 # MM gal/year
    get_MESP = lambda: tea.solve_price(ethanol)*ethanol_density_kggal # from $/kg to $/gallon
    get_GWP = lambda: sys.get_net_impact('GWP')/sys.operating_hours/ethanol.F_mass*ethanol_density_kggal

    print(f'annual ethanol: ${get_ethanol():.3f} MM gal/yr')
    print(f'price: ${get_MESP():.2f}/gal')
    print(f'GWP: {get_GWP():.2f} kg CO2e/gal')
    
    return get_ethanol(), get_MESP(), get_GWP(),
    
# Due to a lack of accurate data on the mass of lignocellulosic waste produced in New Jersey, we will look at the number of farmers who surveyed in New Jersey and the average farm size in New Jersey to use biomass in their renewable energy production.
# Data from 2017: https://www.nass.usda.gov/Publications/AgCensus/2017/Full_Report/Volume_1,_Chapter_2_County_Level/New_Jersey/st34_2_0043_0043.pdf
# Harvested biomass for use in renewable energy production: 116 farms
# Atlantic: 4
# Bergen: 0
# Burlington: 1
# Camden: 0
# Cape May: 0
# Cumberland: 2
# Essex: 0
# Gloucester: 3
# Hudson: 0
# Hunterdon: 19
# Mercer: 3
# Middlesex: 6
# Monmouth: 10
# Morris: 13
# Ocean: 2



def county(name, state_data=STATE_DATA):
    # check if the name inputted in county exists in the first column of state_data
    
    name_final = None
    
    for item in state_data['County']:
        if item.lower() == name.lower():
            name_final = item
            break
        
    if name_final is None:
        return None

    # locate the 'Kilogram/hr' value for the specific county
    dry_tonnes = int(state_data.loc[state_data['County'] == name_final, 'Lignocellulose (dry tons)'].values[0])
    kg_per_hr = state_data.loc[state_data['County'] == name_final, 'Kilogram/hr'].values[0]

    ethanol, price, gwp = calculate_annual_ethanol_price_GWP(kg_per_hr)

    return name_final, dry_tonnes, round(ethanol, 3), round(price, 3), round(gwp, 3)
    
def county_data_export_csv(name, df):
    
    name_final = None
    
    for item in df['County']:
        if item.lower() == name.lower():
            name_final = item
            break
        
    if name_final is None:
        return None

    # Return the data for the specific county in a pandas dataframe
    return df.loc[df['County'] == name_final]

if __name__ == '__main__':
    
    df1 = pd.read_csv(r"backend\fermentation\biomass_imperial.csv")
    df2 = pd.read_csv(r"backend\fermentation\biomass_metric.csv")
    
    print(county('cape may'))
    
    print(county_data_export_csv('cape may', df1))
    print(county_data_export_csv('cape may', df2))