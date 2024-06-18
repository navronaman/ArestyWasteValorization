# Imports from backend file
from backend import county, calculate_annual_ethanol_price_GWP

# Imports from flask
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

# For client ID and client secret
# from dotenv import load_dotenv
import secrets

# Additional imports for CSV file sendings
import pandas as pd

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
CORS(app)

FILE_PATH_IMPERIAL = "new_data_imperial.csv"
FILE_PATH_METRIC = "new_data_metric.csv"
    
@app.route('/county/<string:countyname>')
def county_data(countyname):
    countyname = countyname.replace("_", " ")
    result = county(countyname)
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
                
@app.route('/mass/<int:mass>')
def mass_data(mass):
    unit = request.headers.get('X-Unit', 'imperial')
    if unit not in ['imperial', 'metric']:
        unit = 'imperial'
    
    try:
        # case switch statements
        match unit:
            case 'imperial':
                # convert mass from short tons into kilograms
                mass = mass * 907.185
                # convert from annual kilograms to hourly kilograms
                mass = mass / (365*24*0.96)
            case 'metric':
                # convert mass from metric tonnes into kilograms
                mass = mass * 1000
                # convert from annual kilograms to hourly kilograms
                mass = mass / (365*24*0.96)
    
        result = calculate_annual_ethanol_price_GWP(mass)
        ethanol, price, gwp = result
        match unit:
            case 'metric':
                ethanol = ethanol * 2.98668849
                price = price / 2.98668849
                gwp = gwp * 2.98668849
        return jsonify({
            "success": "true",
            "mass": mass,
            "ethanol": round(ethanol, 3),
            "price": round(price, 3),
            "gwp": round(gwp, 3)
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

