# Imports from backend file
from backend.fermentation.lignocellulose import lignocellulose_county, lignocellulose_calc
from backend.htl.liquefaction import htl_county, htl_calc, htl_convert_sludge_mass_kg_hr
from backend.combustion.combustion import combustion_county, combustion_calc
from backend.digestion.anaerobic_digestion import ad_county, ad_calc

# Imports from flask
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

# For client ID and client secret
import secrets

# Additional imports for CSV file sendings
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
CORS(app)

FILE_PATH_IMPERIAL = os.path.abspath(r"backend/fermentation/biomass_imperial.csv")
FILE_PATH_METRIC = os.path.abspath(r"backend/fermentation/biomass_metric.csv")

ETHANOL_DENSITY_KG_GAL_CONVERSION = 2.98668849
KG_TO_LBS_CONVERSION = 2.20462

GAL_TO_M3D_CONVERSION = 0.00378541
GAL_TO_KG_CONVERSION = 0.838*3.78541
MGD_TO_KG_CONVERSION = 3785411.784; # 1 MGD = 3785411.784 kg



"""
In all Fermentation JSON data, there should be these 4 things     
    1. Mass of feedstock in short tons                            
    2. Ethanol produced in MM gallons/year                           
    3. Price of ethanol in $/gallon                               
    4. Greenhouse gas emissions in lb CO2e/gallon                 
"""
# county and mass for fermentation
@app.route('/fermentation-county/<string:countyname>')
def fermentation_county_data(countyname):
    countyname = countyname.replace("_", " ")
    result = lignocellulose_county(countyname)
    if result is None:
        return jsonify({
            "error": "County not found"
        })
    else :
        name, tonnes, ethanol, price, gwp = result
        return jsonify({
            "name": name,
            "tons": tonnes,
            "ethanol": ethanol,
            "price": price,
            "gwp": gwp
        })
                
@app.route('/fermentation-biomass/<int:mass>')
def fermentation_biomass_data(mass):
    unit = request.headers.get('X-Unit', 'tons')
    if unit not in ['tons', 'tonnes']: # in case the header has something other than 'tons' or 'tonnes'
        unit = 'tons' # default to 'tons'
    
    try:
        # case switch statements
        match unit:
            case 'tons':
                tonnes = mass
                # convert mass from short tons into kilograms
                mass = mass * 907.185
                # convert from annual kilograms to hourly kilograms
                mass = mass / (365*24*0.96)
            case 'tonnes':
                tonnes = mass / 0.907185
                # convert mass from metric tonnes into kilograms
                mass = mass * 1000
                # convert from annual kilograms to hourly kilograms
                mass = mass / (365*24*0.96)
    
        result = lignocellulose_calc(mass)
        ethanol, price, gwp = result

        return jsonify({    
            "success": "true",
            "tons": tonnes, # In dry tones
            "ethanol": ethanol, # In gallons
            "price": price, # In $/gallon
            "gwp": gwp # In lb CO2e/gallon
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": str(e)
        })
        
"""
In all HTL County JSON data, there should be these 4 things which are returned as a JSON object  
    1. Name of the county
    2. Sludge of feedstock in dry metric tonnes in that county
    3. Price of diesel in $/gallon
    4. Global warming potential of diesel in lb CO2/gallon
"""

# county for htl
@app.route('/htl-county/', methods=['GET'])
def htl_county_data():
    """
    Takes a county name from the fetch request and returns the data for that county.
    
    URL Format - GET /htl-county?countyname=Cape+May
    
    Query Parameters
    ----------
    countyname : str (required)
        The name of the county.
    
    Returns
    -------
    JSON
        A JSON object that contains:
        1. Name of the county
        2. Sludge of feedstock in dry metric tonnes
        3. Price of diesel in $/gallon
        4. Global warming potential of diesel in lb CO2/gallon
    
    Example
    -------
    /htl-county?countyname=Cape+May
    >>> {
        "gwp": 476.7758239771914,
        "name": "Cape May",
        "price": 457.70631665901186,
        "sludge": 3172.7
    }
    
        
    """
    countyname = request.args.get('countyname', None)
    
    if not countyname:
        return make_response(
            jsonify({"error": "County name not provided"}), 400 # Bad request, no county name
        )
    
    try:
        result = htl_county(countyname)
    except ValueError:
        return make_response(
            jsonify({"error": "County not found"}), 404 # County not found error
        )
    except TypeError as e:
        return make_response(
            jsonify({"error": str(e)}), 400 # Bad request, non-string county
        )
    
    if result:
        name, sludge, price, gwp = result
        response_data = {
            "name": name,
            "sludge": sludge, # In DMT
            "price": price, # In $/gallon
            "gwp": gwp # In lb CO2e/gallon            
        }
        return make_response(
            jsonify(response_data), 200 # Returns a success status code
        )
        
    return make_response(
        jsonify({"error": "Unexpected error"}), 500 # Unknown error
    )
    
    
# mass for htl       
@app.route('/htl-sludge/', methods=['GET'])
def htl_sludge_data():
    """
    Take mass of a feedstock in dry metric tonnes and returns the data containing price of diesel in $/gallon and the global warming potential of diesel in lb CO2/gallon.
    If the unit is in a different unit, convert it into kg/hr and then pass it through the function.
    
    URL Format - GET /htl-sludge?sludge=500&unit=MGD
    
    Query Parameters
    ----------
    sludge : int (required)
        The mass of the feedstock - Depending on the unit
    unit : str (optional)
        The unit of the mass of the feedstock. Default is 'kghr'. 
        Options - 'kghr', 'tons', 'tonnes', 'mgd', 'm3d' [kg/hr, short tons per year, metric tonnes per year, million gallons per day, metric cubes per day]
        
    Returns
    -------
    JSON
        All JSON data contains
        1. Sludge of feedstock in dry metric tonnes
        2. Price of diesel in $/gallon
        3. Global warming potential of diesel in lb CO2/gallon
        
    Examples
    --------
    /htl-sludge?sludge=500&unit=tons
    >>> {
        "gwp": 1183425.480983743,
        "price": 1152386.6057882837,
        "sludge": 51.779965753424655
    }
    /htl-sludge?sludge=500
    >>> {
        "gwp": 122566.64886470242,
        "price": 119410.96966104512,
        "sludge": 500.0
    }
    
    """
    
    sludge = request.args.get('sludge', None)
    
    if sludge is None:
        return make_response(
            jsonify({"error": "Sludge not provided"}), 400 # Bad request, no sludge
        )
    
    unit = request.args.get('unit', 'kghr')
    
    try:
        sludge = float(sludge)
    except ValueError:
        return make_response(
            jsonify({"error": "Sludge should be a number"}), 400 # Bad request, non-float sludge
        )
    
    kg_hr = htl_convert_sludge_mass_kg_hr(sludge, unit)
    
    try:
        result = htl_calc(sludge)
    except TypeError as e:
        return make_response(
            jsonify({"error": str(e)}), 400 # Bad request, non-float sludge
        )
        
    if result:
        price, gwp = htl_calc(kg_hr)
        response_data = {
            "sludge": kg_hr, # In kg/hr
            "price": price, # In $/gallon
            "gwp": gwp # In lb CO2e/gallon
        }
        return make_response(
            jsonify(response_data), 200 # Returns a success status code
        )
    
    return make_response(
        jsonify({"error": "Unexpected error"}), 500 # Unknown error
    )

"""
In all Combustion JSON data, there should be these 5 things
    1. Mass of feedstock in kg/hr
    2. Electricity produced in kWh
    3. Greenhouse gas emissions in kg CO2e
    4. Percent of total emissions
    5. Waste type of the requested data [food, sludge, fog, green, manure]
"""

# county and mass for combustion
@app.route('/combustion-county/<string:countyname>')
def combustion_county_data(countyname):
    waste_type = request.headers.get('X-WasteType', 'sludge')
    countyname = countyname.replace("_", " ")
    
    if waste_type not in ['sludge', 'food', 'fog', 'green', 'manure']:
        waste_type = 'food' # default to 'food'
        
    result = combustion_county(countyname, waste_type)
    if result is None:
        return jsonify({
            "error": "County not found"
        })
    else:
        name, waste_type2, mass, electricity, emissions, percent = result
        return jsonify({
            "name": name, # County name
            "waste_type": waste_type2, # Waste type - sludge, food, fog, green and manure
            "mass": int(mass), # In kg/hr
            "electricity": electricity, # In kWh
            "emissions": emissions, # In kg CO2e
            "percent": percent, # In percentage
        })

@app.route('/combustion-mass/<int:mass>')
def combustion_mass_data(mass):
    
    waste_type = request.headers.get('X-WasteType', 'sludge')
    unit = request.headers.get('X-WasteTypeUnit', 'tons')
    
    if waste_type not in ['sludge', 'food', 'fog', 'green', 'manure']:
        waste_type = 'food' # default to 'food'
    
    if unit not in ['tons', 'tonnes', 'MGD', 'm3/d']:
        unit = 'tons' # default to 'tons'
        
    mass_kg_hr = 0
    match unit:
        case 'tons':
            # convert mass from short tons into kg/hr
            mass_kg_hr = mass * 907.185 / (365*24)
        case 'tonnes':
            # convert mass from metric tonnes into kg/hr
            mass_kg_hr = mass * 1000 / (365*24)
        case 'MGD':
            # convert mass from MGD into kg/hr
            mass_kg_hr = (mass * MGD_TO_KG_CONVERSION) / 24
        case 'm3/d':
            # convert mass from m3/d into MGD first
            mass_kg_hr = mass / (GAL_TO_M3D_CONVERSION * 1e6 )
            # convert mass from MGD into kg/hr            
            mass_kg_hr = (mass_kg_hr * MGD_TO_KG_CONVERSION) / 24
            
    result = combustion_calc(mass_kg_hr, waste_type)
    try:
        if result is None:
            return jsonify({
                "success": "false",
            })
        else:
            waste_type2, mass_kg_hr2, electricity, emissions, percent = result
            
            return jsonify({
                "success": "true", 
                "original_mass": mass, # In tons, tonnes, MGD or m3/d
                "waste_type": waste_type2, # Waste type - sludge, food, fog, green and manure
                "unit": unit, # Unit of the original mass
                "mass": mass_kg_hr, # In kg/hr
                "electricity": electricity, # In kWh
                "emissions": emissions, # In kg CO2e
                "percent": percent, # In percentage
            })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": str(e)
        })

"""
In all Anaerobic Digestion JSON data, there should be these 4 things
    1. Mass of the feedstock in kg/hr
    2. Electricity produced in kWh 
    3. Greenhouse gas emissions in kg CO2e (metric tonnes)
    4. Waste type of the requested data [food, animal, composite wastewater]
"""

# county and mass for anaerobic digestion
@app.route('/anaerobic-digestion-county/<string:countyname>')
def ad_county_data(countyname):
    waste_type = request.headers.get('X-WasteType', 'sludge')
    countyname = countyname.replace("_", " ")
    
    if waste_type not in ['food', 'animal', 'water']:
        waste_type = 'food' # default to 'food' waste
        
    result = ad_county(countyname, waste_type)
    try:
        if result is None:
            return jsonify({
                "error": "County not found"
            })
        else:
            name, waste_type2, mass, electricity, emissions, percent = result
            return jsonify({
                "name": name, # County name
                "waste_type": waste_type2, # Waste type - food, animal, composite wastewater
                "mass": int(mass), # In kg/hr
                "electricity": electricity, # In kWh
                "emissions": emissions, # In kg CO2e
                "percent": percent, # In percentage
            })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route('/anaerobic-digestion-mass/<int:mass>')
def ad_mass_data(mass):
    
    waste_type = request.headers.get('X-WasteType', 'food')
    unit = request.headers.get('X-WasteTypeUnit', 'tons')
    
    if waste_type not in ['food', 'animal', 'water']:
        waste_type = 'food' # default to 'food'
        
    if unit not in ['tons', 'tonnes', 'MGD', 'm3/d']:
        unit = 'tons'
    
    mass_kg_hr = 0
    match unit:
        case 'tons':
            # convert mass from short tons into kg/hr
            mass_kg_hr = mass * 907.185 / (365*24)
        case 'tonnes':
            # convert mass from metric tonnes into kg/hr
            mass_kg_hr = mass * 1000 / (365*24)
        case 'MGD':
            # convert mass from MGD into kg/hr
            mass_kg_hr = (mass * MGD_TO_KG_CONVERSION) / 24
        case 'm3/d':
            # convert mass from m3/d into MGD first
            mass_kg_hr = mass / (GAL_TO_M3D_CONVERSION * 1e6 )
            # convert mass from MGD into kg/hr
            mass_kg_hr = (mass_kg_hr * MGD_TO_KG_CONVERSION) / 24
            
    result = ad_calc(mass_kg_hr, waste_type)
    try:
        if result is None:
            return jsonify({
                "success": "false",
            })
        else:
            waste_type2, mass_kg_hr2, electricity, emissions, percent = result
            return jsonify({
                "success": "true", 
                "original_mass": mass, # In tons, tonnes, MGD or m3/d
                "waste_type": waste_type2, # Waste type - food, animal, composite wastewater
                "unit": unit, # Unit of the original mass
                "mass": mass_kg_hr, # In kg/hr
                "electricity": electricity, # In kWh
                "emissions": emissions, # In kg CO2e
                "percent": percent, # In percentage
            })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": str(e)
        })
            
    

@app.route('/csv')
def export_csv():
    unit = request.headers.get('X-Unit', 'imperial')
    match unit:
        case 'true':
            file_path = FILE_PATH_IMPERIAL
        case 'false':
            file_path = FILE_PATH_METRIC
        case _:
            file_path = FILE_PATH_IMPERIAL
    
    df = pd.read_csv(file_path)
    csv_string = df.to_csv(index=False)
    
    output = make_response(csv_string)
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/csv/<string:countyname>')
def county_data_export_csv(countyname):
    
    unit = request.headers.get('X-Unit', 'imperial')
    match unit:
        case 'true':
            file_path = FILE_PATH_IMPERIAL
        case 'false':
            file_path = FILE_PATH_METRIC
        case _:
            file_path = FILE_PATH_IMPERIAL
    
    county = countyname.replace("_", " ").title()
    print(county)
    df = pd.read_csv(file_path)
    df = df.loc[df['County'] == county]
    csv_string = df.to_csv(index=False)
    
    output = make_response(csv_string)
    output.headers["Content-Disposition"] = f"attachment; filename={countyname}_data.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True)

