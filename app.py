# Imports from backend file
from backend.fermentation.lignocellulose import lignocellulose_county, lignocellulose_calc
from backend.htl.liquefication import htl_county, htl_calc
from backend.combustion.combustion import combustion_county, combustion_calc

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

GAL_TO_M3D_CONVERSION = 0.12845
GAL_TO_KG_CONVERSION = 0.838*3.78541

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
                tonnes = mass / 907.185
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
In all HTL JSON data, there should be these 4 things     
    1. Sludge of feedstock in MGD (Million Gallons per Day)     
    3. Price of ethanol in $/gallon                               
    4. Greenhouse gas emissions in lb CO2e/gallon                 
"""

# county and mass for htl
@app.route('/htl-county/<string:countyname>')
def htl_county_data(countyname):
    countyname = countyname.replace("_", " ")
    result = htl_county(countyname)
    if result is None:
        return jsonify({
            "error": "County not found"
        })
    else :
        name, sludge, price, gwp = result
        return jsonify({
            "name": name,
            "sludge": sludge,
            "price": price,
            "gwp": gwp
        })
        
@app.route('/htl-sludge/<int:sludge>')
def htl_sludge_data(sludge):
    unit = request.headers.get('X-Unit', 'imperial')
    if unit not in ['imperial', 'metric']:
        unit = 'imperial'
    
    try:
        # case switch statements
        match unit:
            case 'metric':
                # convert from m3/d to MGD
                sludge = sludge / (GAL_TO_M3D_CONVERSION*1e6)
            case 'imperial':
                None
    
        result = htl_calc(sludge)
        price, gwp = result

        # match unit:
        #     case 'metric':
        #         price = price/GAL_TO_KG_CONVERSION # convert from $/gal to $/kg
        #         gwp = gwp/(GAL_TO_KG_CONVERSION*KG_TO_LBS_CONVERSION) # convert from lb CO2/gal to kg CO2/gal
                
        return jsonify({
            "success": "true",
            "sludge": sludge, # In MGD
            "price": price, # In $/gallon
            "gwp": gwp # In lb CO2e/gallon
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": str(e)
        })

# county and mass for combustion
@app.route('/combustion-county/<string:countyname>')
def combustion_county_data(countyname):
    waste_type = request.headers.get('X-WasteType', 'sludge')
    countyname = countyname.replace("_", " ")
    
    print(waste_type)
    
    result = combustion_county(countyname, waste_type)
    if result is None:
        return jsonify({
            "error": "County not found"
        })
    else:
        name, waste_type2, mass, electricity, emissions, percent = result
        return jsonify({
            "name": name,
            "waste_type": waste_type2,
            "mass": int(mass),
            "electricity": electricity,
            "emissions": emissions,
            "percent": percent,
        })

@app.route('/combustion-mass/<int:mass>')
def combustion_mass_data(mass):
    return jsonify({
        "error": "Not implemented"
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

