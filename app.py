# Imports from backend file
from backend import county

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
    
@app.route('/<string:countyname>')
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
    
if __name__ == '__main__':
    app.run(debug=True)

