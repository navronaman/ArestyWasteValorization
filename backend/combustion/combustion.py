import biosteam as bst
from exposan import htl
from biorefineries.cane import create_sugarcane_chemicals
from biorefineries.tea import create_cellulosic_ethanol_tea

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
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

def combustion_calc_raw(mass_in_kg_hr, composition=[0.7, 0.257, 0.204, 0.463], nj_avg_power_co2=486.63):
    """
    Calculates the annual electricity production and avoided emissions based on the composition of water, ash, lipids, and proteins in the feedstock.
    
    Parameters
    ----------
    mass_in_kg_hr: float
        Mass flow rate in kg/hr
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
    >>> combustion_calc(1000, [0.7, 0.257, 0.204, 0.463], 486.63)
    (16771611.411033249, 3.7020225242133353, 0.037930558649726796)
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
    chems = create_chemicals() # Create chemicals, this code is important
    feedstock = bst.Stream('feedstock',
                           Water=a*mass_in_kg_hr, # Moisture is a% of mass flow rate, kg/hr
                            Ash=b*mass_in_kg_hr, # Ash is b% of mass flow rate, kg/hr
                            Lipids=c*(mass_in_kg_hr*(1-a-b)), # Of the remaining non-moisture, non-ash, c% is lipids, kg/hr
                            Proteins=d*(mass_in_kg_hr*(1-a-b)), # Of the remaining non-moisture, non-ash, d% is proteins, kg/hr
                            Carbohydrates=(1-c-d)*(mass_in_kg_hr*(1-a-b))) # Of the remaining non-moisture, non-ash, the rest is carbohydrates, kg/hr
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
    
COMPOSITIONS = {
    'sludge': [0.7, 0.257, 0.204, 0.463], 
    'food': [0.74, 0.0679, 0.22, 0.2],
    'fog': [0.35, 0.01865, 0.987, 0.002], 
    'green': [0.342, 0.134, 0.018, 0.049],
    'manure': [0.6634, 0.3056, 0.092325, 0.216375],
    }

def combustion_calc(mass, waste_type, compositions=COMPOSITIONS):
    """
    Calculates the annual electricity production and avoided emissions from combustion of sludge, food waste, FOG, or green manure.
    
    Parameters
    ----------
    mass : float
        Mass flow rate in kg/hr
    waste_type : str
        Type of waste, must be one of 'sludge', 'food', 'fog', 'green', or 'manure'
    compositions : dict
        Dictionary containing the compositions of water, ash, lipids, and proteins for each waste type
        
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
    ValueError
        If waste_type is not one of 'sludge', 'food', 'fog', 'green', or 'manure'
    TypeError
        If waste_type is not a string
    TypeError
        If mass is not a float or an int
    ValueError
        If compositions is not a dict
        
    Examples
    --------
    >>> combustion_calc(1000, "sludge")
    (16771611.411033249, 3.7020225242133353, 0.037930558649726796)
        
    """
    
    # raising the TypeErrors
    if not isinstance(waste_type, str):
        raise TypeError("waste_type must be a string")
    if not isinstance(mass, (float, int)):
        raise TypeError("mass must be a float or an int")
    if not isinstance(compositions, dict):
        raise ValueError("compositions must be a dict")
    
    waste_type = waste_type.lower()
    
    match waste_type:
        case "sludge":
            list_to_use = compositions['sludge']
            mass = mass / list_to_use[0] # convert from dry to total
            return combustion_calc_raw(mass, list_to_use)
        case "food":
            list_to_use = compositions['food']
            mass = mass / list_to_use[0] # convert from dry to total
            return combustion_calc_raw(mass, list_to_use)
        case "fog":
            list_to_use = compositions['fog']
            mass = mass / list_to_use[0] # convert from dry to total
            return combustion_calc_raw(mass, list_to_use)
        case "green":
            list_to_use = compositions['green']
            mass = mass / list_to_use[0] # convert from dry to total
            return combustion_calc_raw(mass, list_to_use)
        case "manure":
            list_to_use = compositions['manure']
            mass = mass / list_to_use[0] # convert from dry to total
            return combustion_calc_raw(mass, list_to_use)
        case _:
            raise ValueError("waste_type must be one of 'sludge', 'food', 'fog', 'green', or 'manure'")
        
STATE_DATA = pd.read_csv(r"backend\combustion\combustion_data.csv")

def combustion_county(county, waste_type, state_data=STATE_DATA):
    """
    Calculates the annual electricity production and avoided emissions from combustion of sludge, food waste, FOG, or green manure in a county.
    
    Parameters
    ----------
    county : str
        County name
    waste_type : str
        Type of waste, must be one of 'sludge', 'food', 'fog', 'green', or 'manure'
    state_data : pd.DataFrame
        DataFrame containing the waste data for each county
        
    Returns
    -------
    county : str
        County name
    annual_electricity : float
        Annual electricity production in MWh
    avoided_emissions : float
        Avoided emissions in million metric tonnes
    avoided_emissions_percent : float
        Avoided emissions as a percentage of total emissions
        
    Raises
    ------
    ValueError
        If waste_type is not one of 'sludge', 'food', 'fog', 'green', or 'manure'
    TypeError
        If waste_type is not a string
    TypeError
        If county is not a string
    TypeError
        If state_data is not a pd.DataFrame
        
    Examples
    --------
    >>> combustion_county("Warren", "sludge")
    (Warren, 16771611.411033249, 3.7020225242133353, 0.037930558649726796)
        
    """
    
    # raising the TypeErrors
    if not isinstance(waste_type, str):
        raise TypeError("waste_type must be a string")
    if not isinstance(county, str):
        raise TypeError("county must be a string")
    if not isinstance(state_data, pd.DataFrame):
        raise TypeError("state_data must be a pd.DataFrame")
        
    name_final = None
    
    for item in state_data['County']:
        if item.lower() == county.lower():
            name_final = item
            break
        
    if name_final is None:
        return None
    
    match waste_type:
        case "sludge":
            mass = state_data.loc[state_data['County'] == name_final, 'Sludge'].values[0] # this is tons | Convert from dry tons/year to kg/hr
            final_mass = mass * 907.185 / (24*365*0.96) # this is dry, which is some percentage of the data
            
        case "food":
            mass = state_data.loc[state_data['County'] == name_final, 'Food (dry tons)'].values[0] # this is tons | Convert from dry tons/year to kg/hr
            final_mass = mass * 907.185 / (24*365*0.96) # this is dry, which is some percentage of the data

        case "fog":
            mass = state_data.loc[state_data['County'] == name_final, 'Fog (dry tons)'].values[0] # this is tons | Convert from dry tons/year to kg/hr
            final_mass = mass * 907.185 / (24*365*0.96) # this is dry, which is some percentage of the data

        case "green":
            mass = state_data.loc[state_data['County'] == name_final, 'Green'].values[0] # this is tons | Convert from dry tons/year to kg/hr
            final_mass = mass * 907.185 / (24*365*0.96) # this is dry, which is some percentage of the data
        case "manure":
            mass = state_data.loc[state_data['County'] == name_final, 'Manure'].values[0] # this is tons | Convert from dry tons/year to kg/hr
            final_mass = mass * 907.185 / (24*365*0.96) # this is dry, which is some percentage of the data

        case _:
            raise ValueError("waste_type must be one of 'sludge', 'food', 'fog', 'green', or 'manure'")
        
    annual_electricity, avoided_emissions, avoided_emissions_percent = combustion_calc(final_mass, waste_type)
    return (
        name_final,
        annual_electricity,
        avoided_emissions,
        avoided_emissions_percent
    )
    
if __name__ == '__main__':
    print(combustion_calc_raw(1000))
    print(combustion_calc(1000, "sludge"))
    
    print(combustion_county("Warren", "sludge"))
    print(combustion_county("cape may", "food"))
    print(combustion_county("Bergen", "fog"))
    print(combustion_county("mIddlesex", "green"))
    print(combustion_county("mercer", "manure"))
