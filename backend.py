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

STATE_DATA = pd.read_csv('data.csv')
STATE_DATA["Kilogram"] = STATE_DATA["Lignocellulose (dry tons)"] * 907.185
STATE_DATA["Kilogram/hr"] = STATE_DATA["Kilogram"] / (365*24*0.96)
STATE_DATA["Annual Ethanol ($ gal/yr)"] = None
STATE_DATA["Price ($/kg)"] = None
STATE_DATA["GWP (kg CO2e/gal)"] = None


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
    
    return get_ethanol(), get_MESP(), get_GWP()
    
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
    if name not in state_data['County'].values:
        return None

    # locate the 'Kilogram/hr' value for the specific county
    kg_per_hr = state_data.loc[state_data['County'] == name, 'Kilogram/hr'].values[0]

    ethanol, price, gwp = calculate_annual_ethanol_price_GWP(kg_per_hr)

    return ethanol, price, gwp    
    

if __name__ == '__main__':

    # print("All of New Jersey")
    # print("Number of farms: 116")
    # n_nj = 116
    # mass_nj = 116*100 # kg/yr
    # calculate_annual_ethanol_price_GWP(mass_nj)

    # print("\nAtlantic County")
    # print("Number of farms: 4")
    # calculate_annual_ethanol_price_GWP(4*100)

    # print("\nBergen County")

    # print("\nBurlington County")
    # calculate_annual_ethanol_price_GWP(1*100)

    # print("\nCamden County")    

    # print("\nCape May County")    

    # print("\nCumberland County")
    # calculate_annual_ethanol_price_GWP(2*100)

    # print("\nEssex County")

    # print("\nGloucester County")
    # calculate_annual_ethanol_price_GWP(3*100)

    # print("\nHudson County")

    # print("\nHunterdon County")
    # calculate_annual_ethanol_price_GWP(19*100)

    # print("\nMercer County")
    # calculate_annual_ethanol_price_GWP(3*100)

    # print("\nMiddlesex County")
    # calculate_annual_ethanol_price_GWP(6*100)

    # print("\nMonmouth County")
    # calculate_annual_ethanol_price_GWP(10*100)

    # print("\nMorris County")
    # calculate_annual_ethanol_price_GWP(13*100)

    # print("\nOcean County")
    # calculate_annual_ethanol_price_GWP(2*100)
    
    print(county('Atlantic'))