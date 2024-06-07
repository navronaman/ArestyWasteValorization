# Imports from backend file
from backend import county, calculate_annual_ethanol_price_GWP, county_data_export_csv

# Imports from flask
from flask import Flask, jsonify, make_response
from flask_cors import CORS

# For client ID and client secret
# from dotenv import load_dotenv
import secrets

# Additional imports for CSV file sendings
import pandas as pd
from io import StringIO

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
CORS(app)

FILE_PATH = "new_data.csv"
    
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
            "tonnes": tonnes,
            "ethanol": ethanol,
            "price": price,
            "gwp": gwp
        })
                
@app.route('/mass/<int:mass>')
def mass_data(mass):
    try:
        result = calculate_annual_ethanol_price_GWP(mass)
        if result is None:
            return jsonify({
                "success": "false",
                "error": "Mass incorrect"
            })
        else:
            ethanol, price, gwp = result
            return jsonify({
                "success": "true",
                "mass": mass,
                "ethanol": ethanol,
                "price": price,
                "gwp": gwp
            })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": str(e)
        })
        
@app.route('/csv')
def export_csv(file_path=FILE_PATH):
    
    df = pd.read_csv(file_path)
    csv_string = df.to_csv(index=False)
    
    output = make_response(csv_string)
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/csv/atlantic')
def county_data_export_csv0(df=FILE_PATH):
    df = pd.read_csv(df)
    df = df.loc[df['County'] == 'Atlantic']
    csv_string = df.to_csv(index=False)
    print(type(csv_string))
    
    output = make_response(csv_string)
    output.headers["Content-Disposition"] = "attachment; filename=atlantic_data.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/csv/<string:countyname>')
def county_data_export_csv(countyname, file_path=FILE_PATH):
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

