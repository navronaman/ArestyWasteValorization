// when the unit button is clicked

var sludgeUnit = "MGD";
var priceUnit = "$/gal";
var gwpUnit = "lb CO2/gal";

var galToM3 = 0.00378541;
var kgToLbsConversion = 2.20462;
var galToMMBTUConversion = 0.12845;
var galToKg = 0.838*3.78541;


function changeSettings(unit) {
    if (unit == "imperial") {

        // change the unit values
        sludgeUnit = "MGD"
        priceUnit = "$/gal"
        gwpUnit = "lb CO2/gal"

        // manual input units in imperial
        document.getElementById('m-sludge').innerHTML = 'MGD (million gallons per day)';
        document.getElementById('m-price-unit').innerHTML = ' /gal';
        document.getElementById('m-gwp-unit').innerHTML = ' (lb CO2 eq/gal):';

        document.getElementById('massInput').min = 1;
        document.getElementById('massInput').max = 2000;
        document.getElementById('massInput').placeholder = "1-2000";

    }

    else if (unit == "metric") {

        // change the unit values
        sludgeUnit = "m3/d"
        priceUnit = "$/kg"
        gwpUnit = "kg CO2/kg"

        // manual input units in metric
        document.getElementById('m-sludge').innerHTML = 'm3/d (cubic meter per day)';
        document.getElementById('m-price-unit').innerHTML = ' /kg';
        document.getElementById('m-gwp-unit').innerHTML = ' (kg CO2 eq/kg):';

        document.getElementById('massInput').min = 10000;
        document.getElementById('massInput').max = 1000000;
        document.getElementById('massInput').placeholder = "10,000-1,000,000";


    }

    console.log(sludgeUnit, priceUnit, gwpUnit);

    // update the drop down menues to reflect the changes
    document.getElementById('sludge-units').value = sludgeUnit;
    document.getElementById('price-units').value = priceUnit;
    document.getElementById('gwp-units').value = gwpUnit;

    updateUnitsEverywhere();
}

// this function is for when a unit is changed in the drop down menus
function updateUnits() {

    // get the unit value from HTML
    sludgeUnit = document.getElementById('sludge-units').value;
    priceUnit = document.getElementById('price-units').value;
    gwpUnit = document.getElementById('gwp-units').value;

    console.log(sludgeUnit, priceUnit, gwpUnit);

    updateUnitsEverywhere();

    // change the values of the data in infoTop and comparison
    if (currentCountyData !== null && previousCountyData !== null) {
        displayInfoTop(currentCountyData);
        displayComparison(previousCountyData, currentCountyData);
    }
    else if (currentCountyData !== null && previousCountyData === null) {
        displayInfoTop(currentCountyData);
        displayComparison(currentCountyData, null);
    }
    else {
        console.log('no data');
    }
}

// this function to update the units everywhere
// and also change the tool tips
function updateUnitsEverywhere() {

    // resetting the manual input units every time the unit is changed
    document.getElementById('m-price').innerHTML = 0;
    document.getElementById('m-gwp').innerHTML = 0;

    /* changes units in two places:
    1. the comparison table headers
    2. the tool tips in the top info div */
    switch (sludgeUnit) {
        case "MGD":
            document.getElementById('r0-sludge').innerHTML = 'Sludge (MGD)';
            document.getElementById('sludge-tool').innerHTML = 'Holding capacity in million gallons a day';
            break;
        case "m3/d":
            document.getElementById('r0-sludge').innerHTML = 'Sludge (m3/d)';
            document.getElementById('sludge-tool').innerHTML = 'Holding capacity in cubic meters a day';
            break;
    }

    switch (priceUnit) {
        case "$/gal":
            document.getElementById('r0-price').innerHTML = 'Price ($/gal):';
            document.getElementById('price-tool').innerHTML = 'Cost of diesel per gallon (Minimum Selling Price)';
            break;
        case "$/kg":
            document.getElementById('r0-price').innerHTML = 'Price ($/kg):';
            document.getElementById('price-tool').innerHTML = 'Cost of diesel per kg (Minimum Selling Price)';
            break;
        case "$/m3":
            document.getElementById('r0-price').innerHTML = 'Price ($/m3):';
            document.getElementById('price-tool').innerHTML = 'Cost of diesel per cubic meter (Minimum Selling Price)';
            break;
        case "$/MMBTU":
            document.getElementById('r0-price').innerHTML = 'Price ($/MMBTU):';
            document.getElementById('price-tool').innerHTML = 'Cost of diesel per million british thermal units (Minimum Selling Price)';
    }

    switch (gwpUnit) {
        case "lb CO2/gal":
            document.getElementById('r0-gwp').innerHTML = 'GWP (lb CO2 eq/gal):';
            document.getElementById('gwp-tool').innerHTML = 'Every gallon of ethanol saves this much CO2 in pounds';
            break;
        case "kg CO2/kg":
            document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/kg):';
            document.getElementById('gwp-tool').innerHTML = 'Every kg of ethanol saves this much CO2 in kg';
            break;
        case "kg CO2/m3":
            document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/m3):';
            document.getElementById('gwp-tool').innerHTML = 'Every cubic meter of ethanol saves this much CO2 in kg';
            break;
        case "kg CO2/MMBTU":
            document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/MMBTU):';
            document.getElementById('gwp-tool').innerHTML = 'Every MMBTU of ethanol saves this much CO2 in kg';
            break;
    }
}

// get info for county
async function getInfo(county) {
    console.log(unit);
    const url = `http://localhost:5000/htl-county/${county}`;
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
    let sludge = data.sludge;
    let price = data.price;
    let gwp = data.gwp;

    document.getElementById('countyName').innerHTML = `${countyname} County`;

    // change the units based on the units selected
    switch (sludgeUnit) {
        case "MGD":
            break;
        case "m3/d":
            sludge = sludge * galToM3 * 1e6; // since the default is in MGD, we multiply by 1e6 to get m3/d
            break;
    }

    switch (priceUnit) {
        case "$/gal":
            break;
        case "$/kg":
            price = price / galToKg; 
            break;
        case "$/m3":
            price = price / galToM3; // divide by 0.00378541 to get $/m3
            break;
        case "$/MMBTU":
            price = price / (galToMMBTUConversion * galToKg); // divide by 0.12845 * 0.838 to get $/MMBTU
            break;
    }

    switch (gwpUnit) {
        case "lb CO2/gal":
            break;
        case "kg CO2/kg":
            gwp = gwp / (kgToLbsConversion * galToKg); // first change the lb to kg, then remove the gal
            break; 
        case "kg CO2/m3":
            gwp = gwp / (kgToLbsConversion * galToM3); // first change the lb to kg, then remove the gal
            break;
        case "kg CO2/MMBTU":
            gwp = gwp / (kgToLbsConversion * galToMMBTUConversion); // first change the lb to kg, then remove the gal
            break;
    }

    sludge = sludge.toFixed(3);
    price = price.toFixed(3);
    gwp = gwp.toFixed(3);    

    console.log(sludge, price, gwp);

    document.getElementById('sludge').innerHTML = sludge;
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

    displayComparisonHelper(data1, 1);

    if (data2 === null){
        document.getElementById('r2-name').innerHTML = 'County 2'
        document.getElementById('r2-sludge').innerHTML = 0
        document.getElementById('r2-price').innerHTML = 0
        document.getElementById('r2-gwp').innerHTML = 0
    }

    else {
        displayComparisonHelper(data2, 2);
    }
}

// this is a helper function for the comparison
function displayComparisonHelper(data, row){
    let countyname = data.name;
    let sludge = data.sludge;
    let price = data.price;
    let gwp = data.gwp;

    // change the units based on the units selected
    switch (sludgeUnit) {
        case "MGD":
            break;
        case "m3/d":
            sludge = sludge * galToM3 * 1e6; // since the default is in MGD, we multiply by 1e6 to get m3/d
            break;
    }

    switch (priceUnit) {
        case "$/gal":
            break;
        case "$/kg":
            price = price / galToKg; 
            break;
        case "$/m3":
            price = price / galToM3; // divide by 0.00378541 to get $/m3
            break;
        case "$/MMBTU":
            price = price / (galToMMBTUConversion * galToKg); // divide by 0.12845 * 0.838 to get $/MMBTU
            break;
    }

    switch (gwpUnit) {
        case "lb CO2/gal":
            break;
        case "kg CO2/kg":
            gwp = gwp / (kgToLbsConversion * galToKg); // first change the lb to kg, then remove the gal
            break; 
        case "kg CO2/m3":
            gwp = gwp / (kgToLbsConversion * galToM3); // first change the lb to kg, then remove the gal
            break;
        case "kg CO2/MMBTU":
            gwp = gwp / (kgToLbsConversion * galToMMBTUConversion); // first change the lb to kg, then remove the gal
            break;
    }

    sludge = sludge.toFixed(3);
    price = price.toFixed(3);
    gwp = gwp.toFixed(3);    

    console.log(sludge, price, gwp);

    document.getElementById(`r${row}-name`).innerHTML = `${countyname} County`
    document.getElementById(`r${row}-sludge`).innerHTML = sludge
    document.getElementById(`r${row}-price`).innerHTML = price
    document.getElementById(`r${row}-gwp`).innerHTML = gwp

}

// Getting mass
function getMassInfo() {
    const massInput = document.getElementById("massInput").value;
    const mass = Number(massInput)

    const min = document.getElementById("massInput").min;
    const max = document.getElementById("massInput").max;

    console.log(mass)

    if (isNaN(mass) || mass < min || mass > max || mass === 0 || !Number.isInteger(mass)){
        document.getElementById("errorMass").innerHTML = `<span class='error'> Please enter a valid number between ${min} and ${max} </span>`;
        return;
    }

    const url = `http://localhost:5000/htl-sludge/${mass}`;
    const options = {
        headers: {
            'X-Unit': unit
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

            const price = data.price;
            const gwp = data.gwp;

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




