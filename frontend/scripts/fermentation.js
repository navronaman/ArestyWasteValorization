
// this function is called when the page is loaded, and used to change the settings once the unit is clicked

var biomassUnit = "tons"; // default unit for biomass
var ethanolUnit = "MM gal/year"; // default unit for ethanol
var priceUnit = "$/gal"; // default unit for price
var gwpUnit = "lb CO2/gal"; // default unit for gwp

var tonToTonne = 0.907185;
var galToKgforEthanol = 2.98668849;
var kgToLbsConversion = 2.20462;
var galToMMBTUConversion = 0.07633; 
// source for MM gal to MMBTU 
// https://h2tools.org/hyarc/calculator-tools/lower-and-higher-heating-values-fuels

function changeSettings(unit) {
    if (unit == "imperial") {

        // change the unit values
        biomassUnit = "tons";
        ethanolUnit = "MM gal/year";
        priceUnit = "$/gal";
        gwpUnit = "lb CO2/gal";

    }
    else if (unit == "metric") {

        // change the unit values
        biomassUnit = "tonnes";
        ethanolUnit = "kilotonnes/year";
        priceUnit = "$/kg";
        gwpUnit = "kg CO2/kg";

    }

    // update the drop down menues to reflect the changes
    document.getElementById('biomass-units').value = biomassUnit;
    document.getElementById('ethanol-units').value = ethanolUnit;
    document.getElementById('price-units').value = priceUnit;
    document.getElementById('gwp-units').value = gwpUnit;
    
    updateUnitsEverywhere(); // this changes the tool tips and the unit values
}

// this function is for when a unit is changed in the drop down menus
function updateUnits() {
    biomassUnit = document.getElementById('biomass-units').value;
    ethanolUnit = document.getElementById('ethanol-units').value;
    priceUnit = document.getElementById('price-units').value;
    gwpUnit = document.getElementById('gwp-units').value;

    updateUnitsEverywhere();

    // change the values of the data in infoTop and comparison
    if (currentCountyData !== null && previousCountyData !== null) {
        displayInfoTop(currentCountyData);
        displayComparison(currentCountyData, previousCountyData);
    }
    else if (currentCountyData !== null && previousCountyData === null) {
        displayInfoTop(currentCountyData);
        displayComparison(currentCountyData, null);
    }
    else {
        console.log('no data');
    }
} 

// this function is used to update the units in all of the HTML
// we also change the tool tips over here
function updateUnitsEverywhere() {
    
    // resetting the manual input units every time the unit is changed
    document.getElementById('m-ethanol').innerHTML = 0;
    document.getElementById('m-price').innerHTML = 0;
    document.getElementById('m-gwp').innerHTML = 0;

    switch (biomassUnit) {
        case "tons":
            document.getElementById('biomass-tool').innerHTML = 'US Short Tons (2000 lbs) are used for measuring the annual lignocellulose'
            document.getElementById('r0-biomass').innerHTML = 'Annual Biomass (tons):';
            break;
        case "tonnes":
            document.getElementById('biomass-tool').innerHTML = 'Metric tonnes (1000 kgs) are used for measuring the annual lignocellulose'
            document.getElementById('r0-biomass').innerHTML = 'Annual Biomass (tonnes):';
            break;
    }

    switch (ethanolUnit) {
        case "MM gal/year":
            document.getElementById('ethanol-tool').innerHTML = 'Annual production in million gallons'
            document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (MM gal/year):';
            break;
        case "tonnes/year":
            document.getElementById('ethanol-tool').innerHTML = 'Annual production in metric tonnes (1000 kgs)'
            document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (tonnes/year):';
            break;
        case "kilotonnes/year":
            document.getElementById('ethanol-tool').innerHTML = 'Annual production in kilotonnes (1M kgs)'
            document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (kilotonnes/year):';
            break;
        case "MMBTU/year":
            document.getElementById('ethanol-tool').innerHTML = 'Annual production in million MMBTU (million british thermal units)'
            document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (MMBTU/year):';
            break;
    }

    switch (priceUnit) {
        case "$/gal":
            document.getElementById('price-tool').innerHTML = 'Cost of ethanol per gallon (Minimum Selling Price)'
            document.getElementById('r0-price').innerHTML = 'Price ($/gal):';
            break;
        case "$/kg":
            document.getElementById('price-tool').innerHTML = 'Cost of ethanol per kg (Minimum Selling Price)'
            document.getElementById('r0-price').innerHTML = 'Price ($/kg):';
            break;
        case "$/MMBTU":
            document.getElementById('price-tool').innerHTML = 'Cost of ethanol per MMBTU (Minimum Selling Price)'
            document.getElementById('r0-price').innerHTML = 'Price ($/MMBTU):';
            break;
    }

    switch (gwpUnit) {
        case "lb CO2/gal":
            document.getElementById('gwp-tool').innerHTML = 'Every gallon of ethanol saves this much CO2 in pounds'
            document.getElementById('r0-gwp').innerHTML = 'GWP (lb CO2/gal):';
            break;
        case "kg CO2/kg":
            document.getElementById('gwp-tool').innerHTML = 'Every kg of ethanol saves this much CO2 in kg'
            document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2/kg):';
            break;
        case "kg CO2/MMBTU":
            document.getElementById('gwp-tool').innerHTML = 'Every MMBTU of ethanol saves this much CO2 in kg'
            document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2/MMBTU):';
            break;
    }

}

// internal function, used to get info about a county
// this info will be set to current county data, and then used to update info and comparison
async function getInfo(county) {
    console.log(unit);
    const url = `http://localhost:5000/fermentation-county/${county}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data);
        currentCountyData = data;
        return data;
    }

    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return null;
    }
}

// this displays the current county data on the top
function displayInfoTop(data){
    let countyname = data.name;
    let tons = data.tons;
    let ethanol = data.ethanol;
    let price = data.price;
    let gwp = data.gwp;

    document.getElementById('countyName').innerHTML = `${countyname} County`;

    // change the units based on the unit selected
    switch (biomassUnit) {
        case "tons":
            break;
        case "tonnes":
            tons = tons * 0.907185;
    }

    switch (ethanolUnit) {
        case "MM gal/year":
            break;
        case "tonnes/year":
            ethanol = ethanol * galToKgforEthanol * 1e3; // since we're converting from million gallons into tonnes
            break;
        case "kilotonnes/year":
            ethanol = ethanol * galToKgforEthanol; 
            break;
        case "MMBTU/year":
            ethanol = ethanol * galToMMBTUConversion;
    }
    
    switch (priceUnit) {
        case "$/gal":
            break;
        case "$/kg":
            price = price / galToKgforEthanol; 
            break;
        case "$/MMBTU":
            price = price / galToMMBTUConversion;
    }

    switch (gwpUnit) {
        case "lb CO2/gal":
            break;
        case "kg CO2/kg":
            gwp = gwp * kgToLbsConversion / galToKgforEthanol;
            break;
        case "kg CO2/MMBTU":
            gwp = gwp * kgToLbsConversion / galToMMBTUConversion;
    }

    tons = tons.toFixed(0);
    ethanol = ethanol.toFixed(3);
    price = price.toFixed(3);
    gwp = gwp.toFixed(3);

    console.log(tons, ethanol, price, gwp);

    document.getElementById('biomass').innerHTML = tons;
    document.getElementById('ethanol').innerHTML = ethanol;
    document.getElementById('price').innerHTML = price;
    document.getElementById('gwp').innerHTML = gwp;

    // highlight the county name
    const countyNameSpan = document.getElementById('countyName');
    countyNameSpan.classList.add('highlight');

    setTimeout(() => {
        countyNameSpan.classList.remove('highlight');
    }, 2000);

}

// this is for the comparison
function displayComparison(data1, data2){

    if (data1 === null){
        return;
    }

    // everything below is assuming that data1 is not null
    let countyname = data1.name;
    let t = data1.tons;
    let ethanol = data1.ethanol;
    let price = data1.price;
    let gwp = data1.gwp;

    if (unit == "metric") {

        console.log('metric unit')
        // this is a metric unit, now we will convert
        t = t * 0.907185;
        t = t.toFixed(1);
        ethanol = ethanol * 2.98668849;
        ethanol = ethanol.toFixed(3);
        price = price / 2.98668849;
        price = price.toFixed(3);
        gwp = gwp / 2.98668849;
        gwp = gwp.toFixed(3);

        console.log(t, ethanol, price, gwp);
    }

    document.getElementById('r1-name').innerHTML = `${countyname} County`
    document.getElementById('r1-biomass').innerHTML = t 
    document.getElementById('r1-ethanol').innerHTML = ethanol
    document.getElementById('r1-price').innerHTML = price
    document.getElementById('r1-gwp').innerHTML = gwp

    // data is always in imperial units
    if (data2 === null){
        document.getElementById('r2-name').innerHTML = 'County 2'
        document.getElementById('r2-biomass').innerHTML = 0
        document.getElementById('r2-ethanol').innerHTML = 0
        document.getElementById('r2-price').innerHTML = 0
        document.getElementById('r2-gwp').innerHTML = 0
    }

    else {
        let countyname2 = data2.name;
        let t2 = data2.tons;
        let ethanol2 = data2.ethanol;
        let price2 = data2.price;
        let gwp2 = data2.gwp;

        if (unit == "metric") {
            t2 = t2 * 0.907185;
            t2 = t2.toFixed(1);
            ethanol2 = ethanol2 * 2.98668849;
            ethanol2 = ethanol2.toFixed(3);
            price2 = price2 / 2.98668849;
            price2 = price2.toFixed(3);
            gwp2 = gwp2 / 2.98668849;
            gwp2 = gwp2.toFixed(3);
        }

        document.getElementById('r2-name').innerHTML = `${countyname2} County`
        document.getElementById('r2-biomass').innerHTML = t2 
        document.getElementById('r2-ethanol').innerHTML = ethanol2
        document.getElementById('r2-price').innerHTML = price2
        document.getElementById('r2-gwp').innerHTML = gwp2
    }
}

// Getting mass
function getMassInfo() {
    const massInput = document.getElementById("massInput").value;
    const mass = Number(massInput)

    if (isNaN(mass) || mass < 1000 || mass > 1000000 || mass === 0 || !Number.isInteger(mass)){
        document.getElementById("errorMass").innerHTML = "<span class='error'> Please enter a valid number between 100 and 100000 </span>";
        return;
    }

    let unitName = "imperial"
    switch (unit) {
        case true:
            unitName = "imperial";
            break;
        case false:
            unitName = "metric";
            break;
    }

    const url = `http://localhost:5000/fermentation-biomass/${mass}`;
    const options = {
        headers: {
            'X-Unit': unitName
        }
    };

    // Example of using fetch with the URL and options
    fetch(url, options)
        .then(response => {
            return response.json()
        })
        .then(data => {
            const success = data.success;
            console.log(data)

            if (!success) {
                document.getElementById("errorMass").innerHTML = "<span class='error'> There was an error with the request </span>";
                return;
            }

            const ethanol = data.ethanol;
            const price = data.price;
            const gwp = data.gwp;

            document.getElementById("m-ethanol").innerHTML = ethanol;
            document.getElementById("m-price").innerHTML = price;
            document.getElementById("m-gwp").innerHTML = gwp;

            document.getElementById("errorMass").innerHTML = "<b></b>";
            document.getElementById("errorExport").innerHTML = "<b></b>";   
            
        })
        .catch(error => console.error('Error:', error));  
}
          

// Getting the two CSV functions
async function exportToCsvMain() {
    try {
        const options = {
            headers: {
                'X-Unit': unit
            }
        };
        const response = await fetch('http://localhost:5000/csv', options);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'export.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function exportToCsvCounty() {
    if (currentCounty === null) {
        document.getElementById("errorExport").innerHTML = "<span class='error'> Please click on a county first </span>";
        return;
    }
    try {
        const options = {
            headers: {
                'X-Unit': unit
            }
        };
        const response = await fetch(`http://localhost:5000/csv/${currentCounty}`, options);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentCounty.toLowerCase()}_county_export.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        document.getElementById("errorMass").innerHTML = "<b></b>";
        document.getElementById("errorExport").innerHTML = "<b></b>";

    }
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }

}