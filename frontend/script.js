// show sidebar
function showSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = 'flex';
}

// hide sidebar
function hideSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = 'none';
}

// let firstCounty = null; // first county selected
// let secondCounty = null; // second county selected
let currentCounty = null; // current county selected
let previousCounty = null; // previous county selected

let currentCountyData = null;
let previousCountyData = null;

let orderOfComparison = true; // true if first county is selected, false if second county is selected

// imperial/metric button
let unit = true;
function selectUnit(imperial_or_metric) {
    console.log(imperial_or_metric);
    if (imperial_or_metric === 'imperial') {
        unit = true;
        document.getElementById('ethanol-unit').innerHTML = 'Annual Ethanol (gal/year):';
        document.getElementById('price-unit').innerHTML = 'Price ($/gal):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (kg CO2 eq/gal):';

        document.getElementById('r0-biomass').innerHTML = 'Annual Biomass (tons):';
        document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (gal/year):';
        document.getElementById('r0-price').innerHTML = 'Price ($/gal):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/gal):';

        document.getElementById('m-biomass').innerHTML = 'tons';
        document.getElementById('m-ethanol-unit').innerHTML = ' (gal/year)';
        document.getElementById('m-price-unit').innerHTML = ' /gal';
        document.getElementById('m-gwp-unit').innerHTML = ' (kg CO2 eq/gal):';

    } 
    else {
        unit = false;

        document.getElementById('ethanol-unit').innerHTML = 'Annual Ethanol (kg/year):';
        document.getElementById('price-unit').innerHTML = 'Price ($/kg):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (kg CO2 eq/kg):';

        document.getElementById('r0-biomass').innerHTML = 'Annual Biomass (tonnes):';
        document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (kg/year):';
        document.getElementById('r0-price').innerHTML = 'Price ($/kg):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/kg):';

        document.getElementById('m-biomass').innerHTML = 'tonnes';
        document.getElementById('m-ethanol-unit').innerHTML = ' (kg/year)';
        document.getElementById('m-price-unit').innerHTML = ' /kg';
        document.getElementById('m-gwp-unit').innerHTML = ' (kg CO2 eq/kg)';

    }

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
    document.getElementById('m-ethanol').innerHTML = 0;
    document.getElementById('m-price').innerHTML = 0;
    document.getElementById('m-gwp').innerHTML = 0;


    console.log(unit);
}

// internal function, used to get info about a county
// this info will be set to current county data, and then used to update info and comparison
async function getInfo(county) {
    console.log(unit);
    const url = `http://localhost:5000/county/${county}`;
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

/*

Most important of code
-It changes the color of the county when the mouse hovers over it
-It also displays the county name when the mouse hovers over it
-It displays the county information when the county is clicked

*/

document.querySelectorAll('.allPaths').forEach(e => {
    e.setAttribute("class", `allPaths ${e.id}`);
    e.addEventListener("mouseover", function () {
        window.onmousemove = function (j) {
            const x = j.clientX;
            const y = j.clientY;
        }
        const classes = e.className.baseVal.replace(/ /g, ".");
        document.querySelectorAll(`.${classes}`).forEach(county => {
            county.style.fill = "#FF9D00";
        });
    });
    e.addEventListener("mouseleave", function () {
        const classes = e.className.baseVal.replace(/ /g, ".");
        document.querySelectorAll(`.${classes}`).forEach(county => {
            county.style.fill = "#ececec";
        });
    });

    e.addEventListener("click", function () {
        if (currentCounty == null){
            console.log("I'm here at one!")

            currentCounty = e.id;

            getInfo(currentCounty).then(currentCountyData => {
                console.log(currentCountyData); // This should log the data returned by getInfo
                displayInfoTop(currentCountyData);
                displayComparison(currentCountyData, null);        
            }).catch(error => {
                console.error('Error fetching data:', error);
            });

        }
        else if (previousCounty == null && e.id !== currentCounty){

            console.log("I'm here at two!")

            previousCounty = currentCounty;
            previousCountyData = currentCountyData;

            currentCounty = e.id;

            getInfo(currentCounty).then(currentCountyData => {
                console.log(currentCountyData); // This should log the data returned by getInfo
                displayInfoTop(currentCountyData);
                displayComparison(previousCountyData, currentCountyData);    
            }).catch(error => {
                console.error('Error fetching data:', error);
            });

        }
        else {

            console.log("I'm here at three!")

            previousCounty = null;
            previousCountyData = null;

            currentCounty = e.id;

            getInfo(currentCounty).then(currentCountyData => {
                console.log(currentCountyData); // This should log the data returned by getInfo
                displayInfoTop(currentCountyData);
                displayComparison(currentCountyData, null);    
            }).catch(error => {
                console.error('Error fetching data:', error);
            });


        }
        document.getElementById("errorMass").innerHTML = "<b></b>";
        document.getElementById("errorExport").innerHTML = "<b></b>";
    });
    
});

// Collapsible content
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.collapsible-header');
    const container = document.querySelector('.collapsible-container');

    header.addEventListener('click', () => {
        container.classList.toggle('active');
    });


});

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

    const url = `http://localhost:5000/mass/${mass}`;
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
        const response = await fetch('http://localhost:5000/csv');
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
        const response = await fetch(`http://localhost:5000/csv/${currentCounty}`);
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