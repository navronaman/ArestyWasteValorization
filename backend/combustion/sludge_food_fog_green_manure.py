import biosteam as bst
from exposan import htl
from biorefineries.cane import create_sugarcane_chemicals
from biorefineries.tea import create_cellulosic_ethanol_tea

class BoilerTurbogenerator(bst.facilities.BoilerTurbogenerator):

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

def combustion_calc(composition=[0.7, 0.257, 0.204, 0.463], nj_avg_power_co2=486.63):
    """
    Calculates the annual electricity production and avoided emissions from combustion of sludge, food waste, FOG, or green manure.
    
    Parameters
    ----------
    composition : list
        [moisture, ash, lipids, proteins] in kg/hr
    nj_avg_power_co2 : float
        Average power plant emissions in lb CO2/MWh
        
    Returns
    -------
    annual_electricity : float
        Annual electricity production in MWh
    avoided_emissions : float
        Avoided emissions in million metric tonnes
    avoided_emissions_percent : float
        Avoided emissions as a percentage of total emissions
        
    Raises
    ------
    TypeError
        If composition is not a list
    TypeError
        If nj_avg_power_co2 is not a float or an int
    ValueError
        If composition does not have 4 elements
    
    Examples
    --------
    >>> combustion_calc([0.7, 0.257, 0.204, 0.463], 486.63)
        
    """
    
    # Error handling
    if not isinstance(composition, list):
        raise TypeError("composition must be a list")
    if not isinstance(nj_avg_power_co2, (float, int)):
        raise TypeError("nj_avg_power_co2 must be a float or an int")
    if len(composition) != 4:
        raise ValueError("composition must have 4 elements")
    
    # Assign values
    a, b, c, d = composition
    e = 1 - a - b - c - d
    feedstock = bst.Stream('feedstock',
                           Water=a, # kg/hr
                            Ash=b, # kg/hr
                            Lipids=c, # kg/hr
                            Proteins=d, # kg/hr
                            Carbohydrates=e) # kg/hr
    BT = BoilerTurbogenerator('BT', ins=feedstock)
    sys = bst.System('sys', path=(BT,))
    BT = sys.flowsheet.unit.BT
    tea = create_cellulosic_ethanol_tea(sys, OSBL_units=[BT])
    sys.simulate()
    
    total_electricity = -BT.net_power # kW (kWh/hr), net production so the original value is negative
    annual_electricity = total_electricity * 365 * 24 / 1e3 # MWh // million watters we can generate per year
    
    NJ_avg_power_CO2 = nj_avg_power_co2 * 0.453592 # lb CO2/MWh to kg CO2/MWh
    avoided_emissions = NJ_avg_power_CO2 * annual_electricity / 1e3 / 1e6 # million metric tonne
    
    avoided_emissions_percent = avoided_emissions / 97.6
                           
    return (
        annual_electricity,
        avoided_emissions,
        avoided_emissions_percent
    )
