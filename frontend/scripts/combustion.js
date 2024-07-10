// when the unit buttons
var wasteType = "sludge"; // changes when the user selects a waste type
var wasteTypeUnit = "tons"; // drop down menu
var electrictyUnit = "mwh";
var emissionsUnit = "tons";
var percentUnit = "%";

// conversion factors

function changeSettings(unit) {
    if (unit == "imperial") {
        wasteTypeUnit = "tons";
        electrictyUnit = "mwh";
        emissionsUnit = "tons";
        percentUnit = "%"; 
    }
    else if (unit == "metric") {
        wasteTypeUnit = "tonnes";
        electrictyUnit = "mwh"; // TODO : get correct unit
        emissionsUnit = "tonnes"; // TODO : get correct unit
        percentUnit = "%"; // TODO : get correct unit
    }

    console.log(wasteTypeUnit, electrictyUnit, emissionsUnit, percentUnit);

    // update drop down menus
    document.getElementById("wastetype-unit").value = wasteTypeUnit;
    document.getElementById("electricity-unit").value = electrictyUnit;
    document.getElementById("emissions-unit").value = emissionsUnit;
    document.getElementById("percent-unit").value = percentUnit;

    updateUnitsEverywhere();
}

function updateUnits() {
    wasteTypeUnit = document.getElementById("wastetype-unit").value;
    electrictyUnit = document.getElementById("electricity-unit").value;
    emissionsUnit = document.getElementById("emissions-unit").value;
    percentUnit = document.getElementById("percent-unit").value;

    console.log(wasteTypeUnit, electrictyUnit, emissionsUnit, percentUnit);

    updateUnitsEverywhere();

    // update units in infoTop
    if (currentCountyData !== null && previousCountyData !== null) {
        displayInfoTop(currentCountyData);
        displayComparison(previousCountyData, currentCountyData);
    }

    // update units in comparison
    else if (previousCountyData !== null && currentCountyData === null) {
        displayInfoTop(currentCountyData);
        displayComparison(previousCountyData, currentCountyData);
    }
    else {
        console.log('no data');
    }

}

function updateUnitsEverywhere() {
    // to be implemented
    null
}

function selectWasteType(waste_type) {
    wasteType = waste_type;
    console.log(wasteType);
}

async function getInfo(county) {
    const url = `http://localhost:5000/combustion-county/${county}`;
    console.log(wasteType);
    const options = {
        headers : {
            'X-WasteType': wasteType,
        }
    }
    try {
        const response = await fetch(url, options);
        const data = await response.json();
        console.log(data);
        currentCountyData = data;
        return data;
    }
    catch (error) {
        console.log(error);
        return null;
    }
}

function displayInfoTop(data){
    let countyName = data.countyName;
    let wasteType2 = data.wasteType;
    let mass = data.mass;
    let electricity = data.electricity;
    let emissions = data.emissions;
    let percent = data.percent;

    document.getElementById("countyName").innerHTML = `${countyName} County`;
    document.getElementById("wastetype-unit").innerHTML = `${wasteType2}:`;
    document.getElementById("wastetype").innerHTML = mass;
    document.getElementById("electricity").innerHTML = electricity;
    document.getElementById("emissions").innerHTML = emissions;
    document.getElementById("percent").innerHTML = percent;
}
