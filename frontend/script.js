async function getInfo(county) {
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

        document.getElementById("info").innerHTML = `<b> ${countyname} County <br>
         Lignocellulosic Biomass: </b> ${dry_tonnes} dry tonnes <br>
         <b> Annual Ethanol ($ gal/year): </b> ${ethanol} <br>
         <b> Price ($/kg): </b> ${price} <br>
         <b> GWP (kg CO2 eq/kg): </b> ${gwp}`;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

// What does the following code do?
// It changes the color of the county when the mouse hovers over it
// It also displays the county name when the mouse hovers over it
// It displays the county information when the county is clicked

let countyIDClickedOnRightNow = null;

document.querySelectorAll('.allPaths').forEach(e => {
    e.setAttribute("class", `allPaths ${e.id}`);
    e.addEventListener("mouseover", function () {
        window.onmousemove = function (j) {
            const x = j.clientX;
            const y = j.clientY;
            document.getElementById("name").style.left = (x + 10) + "px";
            document.getElementById("name").style.top = (y - 60) + "px";
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
        document.getElementById("name").style.opacity = 0;
    });

    e.addEventListener("click", function () {
        getInfo(e.id);
        document.getElementById("errorMass").innerHTML = "<b></b>";
        document.getElementById("errorExport").innerHTML = "<b></b>";
        countyIDClickedOnRightNow = e.id;
    });
});

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

async function exportToCsv() {
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
        document.bodu.removeChild(a);
    }
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function exportToCsv2() {
    if (countyIDClickedOnRightNow === null) {
        document.getElementById("errorExport").innerHTML = "<span class='error'> Please click on a county first </span>";
        return;
    }
    try {
        const response = await fetch(`http://localhost:5000/csv/${countyIDClickedOnRightNow}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${countyIDClickedOnRightNow.toLowerCase()}_county_export.csv`;
        document.body.appendChild(a);
        a.click();
        document.bodu.removeChild(a);
        document.getElementById("errorMass").innerHTML = "<b></b>";
        document.getElementById("errorExport").innerHTML = "<b></b>";

    }
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }

}


