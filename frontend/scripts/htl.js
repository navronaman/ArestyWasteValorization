// when the unit button is clicked
function changeSettings(unit) {
    if (unit == "imperial") {

        // infoTop units in imperial
        document.getElementById('sludge-unit').innerHTML = '(MGD):';
        document.getElementById('price-unit').innerHTML = 'Price ($/gal):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (lb CO2 eq/gal):';

        // comparison units in imperial
        document.getElementById('r0-sludge').innerHTML = 'Sludge (MGD)';
        document.getElementById('r0-price').innerHTML = 'Price ($/gal):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (lb CO2 eq/gal):';

        // manual input units in imperial
        document.getElementById('m-sludge').innerHTML = 'MGD (million gallons per day)';
        document.getElementById('m-price-unit').innerHTML = ' /gal';
        document.getElementById('m-gwp-unit').innerHTML = ' (lb CO2 eq/gal):';

        // tool tips from the infoTop
        document.getElementById('sludge-tool').innerHTML = 'Holding capacity in million gallons a day'
        document.getElementById('price-tool').innerHTML = 'Cost of diesel per gallon (Minimum Selling Price)'
        document.getElementById('gwp-tool').innerHTML = 'Global Warming Potential per MMBTU'

    }

    else if (unit == "metric") {

        // infoTop units in metric
        document.getElementById('sludge-unit').innerHTML = '(MGD):';
        document.getElementById('price-unit').innerHTML = 'Price ($/kg):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (kg CO2 eq/kg):';

        // comparison units in metric
        document.getElementById('r0-sludge').innerHTML = 'Sludge (MGD)';
        document.getElementById('r0-price').innerHTML = 'Price ($/kg):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/kg):';

        // manual input units in metric
        document.getElementById('m-sludge').innerHTML = 'MGD (million gallons per day)';
        document.getElementById('m-price-unit').innerHTML = ' /kg';
        document.getElementById('m-gwp-unit').innerHTML = ' (kg CO2 eq/kg):';

        // tool tips from the infoTop
        document.getElementById('sludge-tool').innerHTML = 'Holding capacity in million gallons a day'
        document.getElementById('price-tool').innerHTML = 'Cost of diesel per gallon (Minimum Selling Price)'
        document.getElementById('gwp-tool').innerHTML = 'Global Warming Potential per MMBTU'
    }

    document.getElementById('m-price').innerHTML = 0;
    document.getElementById('m-gwp').innerHTML = 0;
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
    document.getElementById('sludge').innerHTML = `${sludge} gal`;
    if (unit == "metric") {

        console.log('metric unit')

        // this is a metric unit, now we will convert
        document.getElementById('sludge').innerHTML = `${sludge} tonnes`; // only because there's a difference in tonnes and tons

    }

    console.log(sludge, price, gwp);

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
    let sludge = data1.sludge;
    let price = data1.price;
    let gwp = data1.gwp;

    if (!unit) {
        // conversions
        null
    }

    document.getElementById('r1-name').innerHTML = `${countyname} County`
    document.getElementById('r1-sludge').innerHTML = sludge
    document.getElementById('r1-price').innerHTML = price
    document.getElementById('r1-gwp').innerHTML = gwp

    // data is always in imperial units
    if (data2 === null){
        document.getElementById('r2-name').innerHTML = 'County 2'
        document.getElementById('r2-sludge').innerHTML = 0
        document.getElementById('r2-price').innerHTML = 0
        document.getElementById('r2-gwp').innerHTML = 0
    }

    else {
        let countyname2 = data2.name;
        let sludge2 = data2.sludge;
        let price2 = data2.price;
        let gwp2 = data2.gwp;

        if (!unit) {
            // conversions
            null
        }

        document.getElementById('r2-name').innerHTML = `${countyname2} County`
        document.getElementById('r2-sludge').innerHTML = sludge2
        document.getElementById('r2-price').innerHTML = price2
        document.getElementById('r2-gwp').innerHTML = gwp2
    }
}

// Getting mass
function getMassInfo() {
    const massInput = document.getElementById("massInput").value;
    const mass = Number(massInput)

    console.log(mass)

    if (isNaN(mass) || mass < 1 || mass > 2000 || mass === 0 || !Number.isInteger(mass)){
        document.getElementById("errorMass").innerHTML = "<span class='error'> Please enter a valid number between 1 and 2000 </span>";
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

    const url = `http://localhost:5000/htl-sludge/${mass}`;
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




