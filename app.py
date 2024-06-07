# Imports from backend file
from backend import county, calculate_annual_ethanol_price_GWP

# Imports from flask
from flask import Flask, jsonify, make_response
from flask_cors import CORS

# For client ID and client secret
# from dotenv import load_dotenv
import secrets

# Additional imports for CSV file sendings
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
        name, ethanol, price, gwp = result
        return jsonify({
            "name": name,
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
    
    output = make_response(file_path)
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    
    
if __name__ == '__main__':
    app.run(debug=True)

