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
from exposan import htl
from biorefineries.cane import create_sugarcane_chemicals
from biorefineries.tea import create_cellulosic_ethanol_tea

class BoilerTurbogenerator(bst.facilities.BoilerTurbogenerator):

    # Make it work for a system without utility agents
    def _load_utility_agents(self):
        steam_utilities = self.steam_utilities
        steam_utilities.clear()
        agent = self.agent
        units = self.other_units
        if units is not None:
            for agent in (*self.other_agents, agent):
                ID = agent.ID
                for u in units:
                    for hu in u.heat_utilities:
                        agent = hu.agent
                        if agent and agent.ID == ID:
                            steam_utilities.add(hu)
            self.electricity_demand = sum([u.power_utility.consumption for u in units])
        else: self.electricity_demand = 0

def create_chemicals():
    htl_cmps = htl.create_components()
    cane_chems = create_sugarcane_chemicals()
    
    # Components in the feedstock
    Water = htl_cmps.Water
    Lipids = htl_cmps.Sludge_lipid.copy('Lipids')
    Proteins = htl_cmps.Sludge_protein.copy('Proteins')
    Carbohydrates = htl_cmps.Sludge_carbo.copy('Carbohydrates')
    Ash = htl_cmps.Sludge_ash.copy('Ash')
    Cellulose = cane_chems.Cellulose
    Hemicellulose = cane_chems.Hemicellulose
    Lignin = cane_chems.Lignin
    CaO = cane_chems.CaO
    
    P4O10 = cane_chems.P4O10
    O2 = cane_chems.O2
    N2 = cane_chems.N2
    CH4 = cane_chems.CH4
    CO2 = cane_chems.CO2
    
    chems = bst.Chemicals((
        Water, Lipids, Proteins, Carbohydrates, Ash,
        Cellulose, Hemicellulose, Lignin, CaO,
        P4O10, O2, N2, CH4, CO2))
    bst.settings.set_thermo(chems)

    return chems

def create_system():
    chems = create_chemicals()
    feedstock = bst.Stream('feedstock', # this is the flow rate that we can change
                            Water=700, # 1000 kg/hr, 0.7*1000=700 | this is moisture
                            Ash=257, # 0.257*1000=257 | this is ash
                            Lipids=204*(1000-700-257)/1e3, # 0.204*(nonmoisture-nonash) = 0.204*(1000-700-257) | this is lipid, part of non-moisture, non-ash
                            Proteins=463*(1000-700-257)/1e3,  # 0.463*(nonmoisture-nonash) = 0.463*(1000-700-257) | this is protein, part of non-moisture, non-ash
                            Carbohydrates=(1000-204-463)*(1000-700-257)/1e3,) # 1000-204-463=333 | this is carbohydrate, part of non-moisture, non-ash
    BT = BoilerTurbogenerator('BT', ins=feedstock)
    sys = bst.System('sys', path=(BT,))
    return sys

# drop down menu to select
# sludge, food, fog, green, manure


# From the HTL module
# water, ash, lipid, protein, carbohydrate
compositions = {
    'sludge': (0.7, 0.257, 0.204, 0.463), # moisture, ash, lipid, protein; lipid/protein in ash-free dry weight
    'food': (0.74, 0.0679, 0.22, 0.2),
    'fog': (0.35, 0.01865, 0.987, 0.002), # fats, oils, and grease
    'green': (0.342, 0.134, 0.018, 0.049),
    'manure': (0.6634, 0.3056, 0.092325, 0.216375),
    }

sys = create_system()
BT = sys.flowsheet.unit.BT
tea = create_cellulosic_ethanol_tea(sys, OSBL_units=[BT])
sys.simulate()

total_electricity = -BT.net_power # kW (kWh/hr), net production so the original value is negative
annual_electricity = total_electricity * 365 * 24 / 1e3 # MWh // million watters we can generate per year
# first output - electricity generated

# NJ averaged CO2 emission, https://www.epa.gov/egrid/data-explorer
NJ_avg_power_CO2 = 486.63 * 0.453592 # lb CO2/MWh to kg CO2/MWh

avoided_emissions = NJ_avg_power_CO2 * annual_electricity / 1e3 / 1e6 # million metric tonne
# absolute number of emisions


# Net GHG emissions of NJ is 97.6 million metric tonnes of CO2e
# https://dep.nj.gov/ghg/nj-ghg-inventory/
avoided_emissions_percent = avoided_emissions / 97.6 
# percentage of avoided emissions


# # This is biogenic CO2, does not count
# emissions = sys.flowsheet.stream.emissions
# total_CO2 = emissions.imass['CO2'] # CO2 emission # kg/hr
# CO2_per_kWh = total_electricity / total_CO2


# everything is in kg/hr