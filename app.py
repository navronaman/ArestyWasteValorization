# Imports from backend file
from backend import county, calculate_annual_ethanol_price_GWP

# Imports from flask
from flask import Flask, render_template, request, redirect, jsonify, session
from flask_cors import CORS

# For client ID and client secret
# from dotenv import load_dotenv
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
CORS(app)

@app.route('/atlantic')
def index():
    ethanol, price, gwp = county('Atlantic')
    return jsonify({
        "ethanol": ethanol,
        "price": price,
        "gwp": gwp
    })
    
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
        
@app.route('/mass')
def mass():
    return jsonify({
        "error": "No mass provided"
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
    
    
if __name__ == '__main__':
    app.run(debug=True)

