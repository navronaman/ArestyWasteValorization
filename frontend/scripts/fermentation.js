
// this function is called when the page is loaded, and used to change the settings once the unit is clicked
function changeSettings(unit) {
    if (unit == "imperial") {

        // infoTop units in imperial
        document.getElementById('ethanol-unit').innerHTML = 'Annual Ethanol (MM gal/year):';
        document.getElementById('price-unit').innerHTML = 'Price ($/gal):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (lb CO2 eq/gal):';

        // comparison units in imperial
        document.getElementById('r0-biomass').innerHTML = 'Annual Biomass (tons):';
        document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (MM gal/year):';
        document.getElementById('r0-price').innerHTML = 'Price ($/gal):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (lb CO2 eq/gal):';

        // manual input units in imperial
        document.getElementById('m-biomass').innerHTML = 'tons';
        document.getElementById('m-ethanol-unit').innerHTML = ' (MM gal/year)';
        document.getElementById('m-price-unit').innerHTML = ' /gal';
        document.getElementById('m-gwp-unit').innerHTML = ' (kg CO2 eq/gal):';

        // tool tips from the infoTop
        document.getElementById('biomass-tool').innerHTML = 'Ethanol production in million gallons per year'
        document.getElementById('ethanol-tool').innerHTML = 'Holding capacity in million gallons a day'
        document.getElementById('price-tool').innerHTML = 'Cost of diesel per gallon (Minimum Selling Price)'
        document.getElementById('gwp-tool').innerHTML = 'Global Warming Potential per MMBTU'

    }
    else if (unit == "metric") {

        // infoTop units in metric
        document.getElementById('ethanol-unit').innerHTML = 'Annual Ethanol (kg/year):';
        document.getElementById('price-unit').innerHTML = 'Price ($/kg):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (kg CO2 eq/kg):';

        // comparison units in metric
        document.getElementById('r0-biomass').innerHTML = 'Annual Biomass (tonnes):';
        document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (kg/year):';
        document.getElementById('r0-price').innerHTML = 'Price ($/kg):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/kg):';

        // manual input units in metric
        document.getElementById('m-biomass').innerHTML = 'tonnes';
        document.getElementById('m-ethanol-unit').innerHTML = ' (kg/year)';
        document.getElementById('m-price-unit').innerHTML = ' /kg';
        document.getElementById('m-gwp-unit').innerHTML = ' (kg CO2 eq/kg)';

        // tool tips from the infoTop
        document.getElementById('biomass-tool').innerHTML = 'Holding capacity in million gallons a day'
        document.getElementById('ethanol-tool').innerHTML = 'Holding capacity in million gallons a day'
        document.getElementById('price-tool').innerHTML = 'Cost of diesel per gallon (Minimum Selling Price)'
        document.getElementById('gwp-tool').innerHTML = 'Global Warming Potential per MMBTU'

    }

    else{
        // energy

        // infoTop units in energy
        document.getElementById('ethanol-unit').innerHTML = 'Annual Ethanol (kg/year):';
        document.getElementById('price-unit').innerHTML = 'Price ($/MMBTU):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (kg CO2 eq/MMBTU):';

        // comparison units in energy
        document.getElementById('r0-biomass').innerHTML = 'Annual Biomass (tonnes):';
        document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (kg/year):';
        document.getElementById('r0-price').innerHTML = 'Price ($/MMBTU):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/MMBTU):';

        // manual input units in energy
        document.getElementById('m-biomass').innerHTML = 'tonnes';
        document.getElementById('m-ethanol-unit').innerHTML = ' (kg/year)';
        document.getElementById('m-price-unit').innerHTML = ' /MMBTU';
        document.getElementById('m-gwp-unit').innerHTML = ' (kg CO2 eq/MMBTU)';

        // tool tips from the infoTop
        document.getElementById('biomass-tool').innerHTML = 'Holding capacity in million gallons a day'
        document.getElementById('ethanol-tool').innerHTML = 'Holding capacity in million gallons a day'
        document.getElementById('price-tool').innerHTML = 'Cost of diesel per gallon (Minimum Selling Price)'
        document.getElementById('gwp-tool').innerHTML = 'Global Warming Potential per MMBTU'

    }

    // resetting the manual input units every time the unit is changed
    document.getElementById('m-ethanol').innerHTML = 0;
    document.getElementById('m-price').innerHTML = 0;
    document.getElementById('m-gwp').innerHTML = 0;
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
    document.getElementById('biomass').innerHTML = `${tons} tons`;
    if (!unit) {

        console.log('metric unit')

        // this is a metric unit, now we will convert
        let tonnes = tons * 0.907185;
        tonnes = tonnes.toFixed(1);

        ethanol = ethanol * 2.98668849;
        ethanol = ethanol.toFixed(3);

        price = price / 2.98668849;
        price = price.toFixed(3);

        gwp = gwp / 2.98668849;
        gwp = gwp.toFixed(3);

        console.log(tonnes, ethanol, price, gwp);

        document.getElementById('biomass').innerHTML = `${tonnes} tonnes`; // only because there's a difference in tonnes and tons

    }

    console.log(tons, ethanol, price, gwp);

    document.getElementById('ethanol').innerHTML = ethanol;
    document.getElementById('price').innerHTML = price;
    document.getElementById('gwp').innerHTML = gwp;

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

    let countyname = data1.name;
    let t = data1.tons;
    let ethanol = data1.ethanol;
    let price = data1.price;
    let gwp = data1.gwp;

    if (!unit) {

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

        if (!unit) {
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