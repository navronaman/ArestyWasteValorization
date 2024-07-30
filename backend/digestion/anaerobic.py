"""
Python script meant to simulate the anaerobic digestion process as modeled by 'AD Screening Tool'.
Refer to the other file for the actual model.
"""


def digester_feedstock_inputs(
    # Required inputs
    project_name, # Name of the project
    project_location, # Location of the project
    project_country, # Country of the project
    feedstock_list, # Type of feedstock [BLUE]
    
    # Default values
    reactor_type="Wet", # In two types - wet and dry [YELLOW]
    reactor_temp="Mesophilic", # In three types - Unheated/Amibient, Mesophilic, Thermophilic [YELLOW]
    post_digestion_dewatering=True, # Whether or not dewatering is used [BLUE]

    
    # Note:
    # Wet AD systems contain 15% 
    #   Unheated/ambient systems are typically operated at 10-20°C
    #   Mesophilic systems are typically operated at 30-40°C
    #   Thermophilic systems are typically operated at 50-60°C
    
    
):
    """
    Instructions:
    
    Please enter your project's information. 
    The information entered in this sheet will be used throughout this workbook. 
    Users must enter data in every cell that is shaded BLUE. 
    This information will be used to generate biogas and digestate production. 
    For every data point the user enters, the user should make a note of the information source 
    or any assumptions made. The tool provides space for the users to make annotations. YELLOW 
    cells represent default values or assumptions. Users do not need to change these values, 
    but are encouraged to do so if local data are available.  There is programed 
    information for over 95 default waste types available for the user to choose from, or 
    they may enter their own.


    Parameters
    ----------
    project_name : str
        Name of the project
    project_location : str
        Location of the project
    project_country : str
        Country of the project
    feedstock_list : list
        This is the format of the list
        [{
            "list": "general",
            "feedstock_type": "Calf,
            "feedstock_totals": 298.46
            "units": "kg/day"
            "user_notes": "This is a note"
            "feedstock_characteristics": {
                "moisture_content": 0.83,
                "total_solids": 0.11,
                "volatile_solids": 0.09,
                "inert_material_and_ash": 0.02,
                "nitrogen_content": 0.05,
                "carbon_content": 0.3001,
                "proteins_percent_of_ts": 0.09,
                "fats_percent_of_ts": 0.02,
                "sugar_and_starches_percent_of_ts": 0.88,
            }
        },
        {
            "list": "specific",
            "feedstock_type": "Calf,
            "feedstock_totals": 298.46
            "units": "kg/day"
            "user_notes": "This is a note"
            "feedstock_characteristics": {
                "moisture_content": 0.9,
                "total_solids": 0.9,
                "volatile_solids": 0.9,
                "inert_material_and_ash": 0.9,
                "nitrogen_content": 0.9,
                "carbon_content": 0.9
                "proteins_percent_of_ts": 0.9,
                "fats_percent_of_ts": 0.9,
                "sugar_and_starches_percent_of_ts": 0.9,
            }
        }]
    
    """