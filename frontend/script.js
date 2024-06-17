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

// imperial/metric button
let unit = true;
function selectUnit(imperial_or_metric) {
    console.log(imperial_or_metric);
    if (imperial_or_metric === 'imperial') {
        unit = true;
        document.getElementById('ethanol-unit').innerHTML = 'Annual Ethanol (gal/year):';
        document.getElementById('price-unit').innerHTML = 'Price ($/gal):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (kg CO2 eq/gal):';

        document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (gal/year):';
        document.getElementById('r0-price').innerHTML = 'Price ($/gal):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/gal):';

        document.getElementById('infoOutput').innerHTML = `
                    <b>Annual Ethanol (gal/year): <br>
                    Price ($/gal): <br>
                    GWP (kg CO2 eq/gal): <br> </b>`
    } 
    else {
        unit = false;

        document.getElementById('ethanol-unit').innerHTML = 'Annual Ethanol (kg/year):';
        document.getElementById('price-unit').innerHTML = 'Price ($/gal):';
        document.getElementById('gwp-unit').innerHTML = 'GWP (kg CO2 eq/kg):';

        document.getElementById('r0-ethanol').innerHTML = 'Annual Ethanol (kg/year):';
        document.getElementById('r0-price').innerHTML = 'Price ($/gal):';
        document.getElementById('r0-gwp').innerHTML = 'GWP (kg CO2 eq/kg):';

        document.getElementById('infoOutput').innerHTML = `
                    <b>Annual Ethanol (kg/year): <br>
                    Price ($/kg): <br>
                    GWP (kg CO2 eq/kg): <br> </b>`
    }
    console.log(unit);
}

// internal function, used to get info about a county
async function getInfo(county, bool) {
    console.log(unit);
    const url = `http://localhost:5000/county/${county}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data);

        const countyname = data.name;
        const tons = data.tons;
        const ethanol = data.ethanol;
        const price = data.price;
        const gwp = data.gwp;

        if (!unit) {
            // this is a metric unit, now we will convert
            const tonnes = tons * 0.907185;
            tonnes = tonnes.toFixed(2);
            ethanol = ethanol * 2.98668849;
            ethanol = ethanol.toFixed(3);
            price = price / 2.98668849;
            price = price.toFixed(2);
            gwp = gwp / 2.98668849;
            gwp = gwp.toFixed(2);

            document.getElementById('biomass').innerHTML = `${tonnes} tonnes`;

        }

        document.getElementById('biomass').innerHTML = `${tons} tons`;
        document.getElementById('ethanol').innerHTML = ethanol;
        document.getElementById('price').innerHTML = price;
        document.getElementById('gwp').innerHTML = gwp;

        const countyNameSpan = document.getElementById('countyName');
        countyNameSpan.classList.add('highlight');

        setTimeout(() => {
            countyNameSpan.classList.remove('highlight');
        }, 2000);

         if (bool){
            document.getElementById('r1-name').innerHTML = `${countyname} County`
            document.getElementById('r1-biomass').innerHTML = `${tons} tons`
            document.getElementById('r1-ethanol').innerHTML = ethanol
            document.getElementById('r1-price').innerHTML = price
            document.getElementById('r1-gwp').innerHTML = gwp

            document.getElementById('r2-name').innerHTML = 'County 2'
            document.getElementById('r2-biomass').innerHTML = '0 tons'
            document.getElementById('r2-ethanol').innerHTML = 0
            document.getElementById('r2-price').innerHTML = 0
            document.getElementById('r2-gwp').innerHTML = 0

        }

        if (!bool){
            document.getElementById('r2-name').innerHTML = `${countyname} County`
            document.getElementById('r2-biomass').innerHTML = `${tons} tons`
            document.getElementById('r2-ethanol').innerHTML = ethanol
            document.getElementById('r2-price').innerHTML = price
            document.getElementById('r2-gwp').innerHTML = gwp
        }
        
    } 
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

/*

Most important of code
-It changes the color of the county when the mouse hovers over it
-It also displays the county name when the mouse hovers over it
-It displays the county information when the county is clicked

*/


let firstCounty = null;
let secondCounty = null;
let currentCounty = null;

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
        if (firstCounty == null){
            console.log("I'm here at one!")

            firstCounty = e.id;

            console.log(firstCounty)
            getInfo(firstCounty, true);
        }
        else if (secondCounty == null && e.id !== firstCounty){
            console.log("I'm here at two!")

            secondCounty = e.id;

            console.log(secondCounty)
            getInfo(secondCounty, false);
        }
        else {
            console.log("I'm here at three!")

            firstCounty = e.id;

            console.log(firstCounty)

            secondCounty = null;
            getInfo(firstCounty, true)
        }
        currentCounty = e.id;
        document.getElementById("errorMass").innerHTML = "<b></b>";
        document.getElementById("errorExport").innerHTML = "<b></b>";
    });
    
});

// Collapsible content
// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.collapsible-header');
    const container = document.querySelector('.collapsible-container');

    header.addEventListener('click', () => {
        container.classList.toggle('active');
    });

    // button.addEventListener('click', () => {
    //     container.classList.toggle('active');
    // });
});



// Getting mass
function getMassInfo() {
    const massInput = document.getElementById("massInput").value;
    const mass = Number(massInput)

    if (isNaN(mass) || mass < 100 || mass > 100000 || mass === 0 || !Number.isInteger(mass)){
        document.getElementById("errorMass").innerHTML = "<span class='error'> Please enter a valid number between 100 and 100000 </span>";
        return;
    }

    const url = `http://localhost:5000/mass/${mass}`;
    fetch(url)
        .then(response => {
            return response.json();
        })
        .then(data => {
            const sucesss = data.success;
            console.log(data);

            if (!sucesss) {
                document.getElementById("errorMass").innerHTML = "<span class='error'> There was an error with the request </span>";
                return;
            }

            const countyname = data.name;
            const ethanol = data.ethanol;
            const price = data.price;
            const gwp = data.gwp;

            document.getElementById("infoOutput").innerHTML = `
         <b> Annual Ethanol (gal/year): </b> ${ethanol} <br>
         <b> Price ($/kg): </b> ${price} <br>
         <b> GWP (kg CO2 eq/kg): </b> ${gwp}`;

         document.getElementById("errorMass").innerHTML = "<b></b>";
         document.getElementById("errorExport").innerHTML = "<b></b>";

        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
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


