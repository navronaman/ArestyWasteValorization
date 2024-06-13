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

// internal function, used to get info about a county
async function getInfo(county, bool) {
    const url = `http://localhost:5000/county/${county}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data);

        const countyname = data.name;
        const dry_tonnes = data.tonnes;
        const ethanol = data.ethanol;
        const price = data.price;
        const gwp = data.gwp;

        document.getElementById('info').innerHTML = `<b><span id='countyName'> ${countyname} County </span><br>
         Lignocellulosic Biomass: </b> ${dry_tonnes} dry tonnes <br>
         <b> Annual Ethanol ($ gal/year): </b> ${ethanol} <br>
         <b> Price ($/kg): </b> ${price} <br>
         <b> GWP (kg CO2 eq/kg): </b> ${gwp}`;

        const countyNameSpan = document.getElementById('countyName');
        countyNameSpan.classList.add('highlight');

        setTimeout(() => {
            countyNameSpan.classList.remove('highlight');
        }, 2000);

         if (bool){
            document.getElementById('r1-name').innerHTML = `${countyname} County`
            document.getElementById('r1-biomass').innerHTML = `${dry_tonnes} tonnes`
            document.getElementById('r1-ethanol').innerHTML = ethanol
            document.getElementById('r1-price').innerHTML = price
            document.getElementById('r1-gwp').innerHTML = gwp

            document.getElementById('r2-name').innerHTML = 'County 2'
            document.getElementById('r2-biomass').innerHTML = '0 tonnes'
            document.getElementById('r2-ethanol').innerHTML = 0
            document.getElementById('r2-price').innerHTML = 0
            document.getElementById('r2-gwp').innerHTML = 0

        }

        if (!bool){
            document.getElementById('r2-name').innerHTML = `${countyname} County`
            document.getElementById('r2-biomass').innerHTML = `${dry_tonnes} tonnes`
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
            document.getElementById("info2").innerHTML = `
                <b>County <br>
                Lignocellulosic Biomass: <br>
                Annual Ethanol ($ gal/year): <br>
                Price ($/kg): <br>
                GWP (kg CO2 eq/kg): </b><br>`;
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

    button.addEventListener('click', () => {
        container.classList.toggle('active');
    });
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
         <b> Annual Ethanol ($ gal/year): </b> ${ethanol} <br>
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


