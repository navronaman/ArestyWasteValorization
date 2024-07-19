// when the unit buttons
var wasteType = "sludge"; // changes when the user selects a waste type
var wasteTypeUnit = "tons"; // drop down menu
var electrictyUnit = "mwh";
var emissionsUnit = "tons";

// conversion factors

function changeSettings(unit) {
    if (unit == "imperial") {
        wasteTypeUnit = "tons";
        emissionsUnit = "tons";
    }
    else if (unit == "metric") {
        wasteTypeUnit = "tonnes";
        emissionsUnit = "tonnes"; // TODO : get correct unit
    }

    console.log(wasteTypeUnit, electrictyUnit, emissionsUnit, percentUnit);

    // update drop down menus
    document.getElementById("wastetype-units").value = wasteTypeUnit;
    document.getElementById("electricity-units").value = electrictyUnit;
    document.getElementById("emissions-units").value = emissionsUnit;

    updateUnitsEverywhere();
}

function updateUnits() {
    wasteTypeUnit = document.getElementById("wastetype-units").value;
    electrictyUnit = document.getElementById("electricity-units").value;
    emissionsUnit = document.getElementById("emissions-units").value;

    console.log(wasteTypeUnit, electrictyUnit, emissionsUnit);

    updateUnitsEverywhere();

}

function updateUnitsForManual() {
    wasteTypeUnit = document.getElementById("m-wastetype-units").value;
    electrictyUnit = document.getElementById("m-electricity-units").value;
    emissionsUnit = document.getElementById("m-emissions-units").value;

    console.log(wasteTypeUnit, electrictyUnit, emissionsUnit);

    updateUnitsEverywhere();
}

function selectWasteType(waste_type) {
    wasteType = waste_type;

    console.log(wasteType);

    updateWasteTypeEverywhere();
}


function updateUnitsEverywhere() {
    // update the drop down menus
    document.getElementById("wastetype-unit").value = wasteTypeUnit;
    document.getElementById("electricity-unit").value = electrictyUnit;
    document.getElementById("emissions-unit").value = emissionsUnit;

    document.getElementById("m-wastetype-units").value = wasteTypeUnit;
    document.getElementById("m-electricity-units").value = electrictyUnit;
    document.getElementById("m-emissions-units").value = emissionsUnit;3

    // update the tool tips and comparion headers
    switch (wasteTypeUnit) {
        case "tons":
            document.getElementById("wastetype-tool").innerHTML = "US short tons (2000 lbs) of waste";
            document.getElementById("r0-wasteunit").innerHTML = "(tons)";
            break;
        case "tonnes":
            document.getElementById("wastetype-tool").innerHTML = "Metric tonnes (1000 kgs) of waste";
            document.getElementById("r0-wasteunit").innerHTML = "(tonnes)";
            break;
        case "MGD":
            document.getElementById("wastetype-tool").innerHTML = "Million gallons per day of waste";
            document.getElementById("r0-wasteunit").innerHTML = "(MGD)";
            break;
        case "m3/d":
            document.getElementById("wastetype-tool").innerHTML = "Cubic meters per day of waste";
            document.getElementById("r0-wasteunit").innerHTML = "(m3/d)";
            break;
    }

    switch (electrictyUnit) {
        case "mwh":
            document.getElementById("electricity-tool").innerHTML = "Megawatt hours of electricity annually generated";
            document.getElementById("r0-electricity").innerHTML = "Annual Electricity (MWh)";
            break;
    }

    switch (emissionsUnit) {
        case "tons":
            document.getElementById("emissions-tool").innerHTML = "Million Short tons (2000 lbs) of CO2 emissions";
            document.getElementById("r0-emissions").innerHTML = "Avoided CO2 Emissions (tons)";
            break;
        case "tonnes":
            document.getElementById("emissions-tool").innerHTML = "Million Metric tonnes (1000 kgs) of CO2 emissions";
            document.getElementById("r0-emissions").innerHTML = "Avoided CO2 Emissions (tonnes)";
            break;
    }

    // update the units
    console.log(wasteTypeUnit, electrictyUnit, emissionsUnit);
    
}

function updateWasteTypeEverywhere() {

    // update the info top section
    // change the options in the drop down menus
    // update the comparison section
    // update the manual input section

    switch (wasteType) {
        case "food":
            document.getElementById("wastetype-name").innerHTML = "Food Waste";
            document.getElementById("wastetype-unit").innerHTML = "Food:";
            document.getElementById("wastetype-units").innerHTML = getDropDownText(1);
            document.getElementById("r0-wastetype").innerHTML = "Food Waste";
            document.getElementById("m-wastetype").innerHTML = "food waste";
            document.getElementById("m-wastetype-units").innerHTML = getDropDownText(1);
            break;
        case "sludge":
            document.getElementById("wastetype-name").innerHTML = "Sludge";
            document.getElementById("wastetype-unit").innerHTML = "Sludge:";
            document.getElementById("wastetype-units").innerHTML = getDropDownText(2);
            document.getElementById("r0-wastetype").innerHTML = "Sludge";
            document.getElementById("m-wastetype").innerHTML = "sludge";
            document.getElementById("m-wastetype-units").innerHTML = getDropDownText(2);
            break;
        case "fog":
            document.getElementById("wastetype-name").innerHTML = "Fats, Oils, and Grease";
            document.getElementById("wastetype-unit").innerHTML = "FOG:";
            document.getElementById("wastetype-units").innerHTML = getDropDownText(1);
            document.getElementById("r0-wastetype").innerHTML = "Fats, Oils, and Grease";
            document.getElementById("m-wastetype").innerHTML = "fats, oils, and grease";
            document.getElementById("m-wastetype-units").innerHTML = getDropDownText(1);
            break;
        case "green":
            document.getElementById("wastetype-name").innerHTML = "Green Waste";
            document.getElementById("wastetype-unit").innerHTML = "Green:";
            document.getElementById("wastetype-units").innerHTML = getDropDownText(1);
            document.getElementById("r0-wastetype").innerHTML = "Green Waste";
            document.getElementById("m-wastetype").innerHTML = "green waste";
            document.getElementById("m-wastetype-units").innerHTML = getDropDownText(1);
            break;
        case "manure":
            document.getElementById("wastetype-name").innerHTML = "Manure";
            document.getElementById("wastetype-unit").innerHTML = "Manure:";
            document.getElementById("wastetype-units").innerHTML = getDropDownText(1);
            document.getElementById("r0-wastetype").innerHTML = "Manure";
            document.getElementById("m-wastetype").innerHTML = "manure";
            document.getElementById("m-wastetype-units").innerHTML = getDropDownText(1);
            break;
    }

    updateUnits();
}

function getDropDownText(no){
    // can either get one or two
    switch (no){
        case 1:
            // this is for food, fog, green and manure
            return `
                <option value="tons">short tons</option>
                <option value="tonnes">metric tonnes</option>
            `;
        case 2:
            // this is for sludge
            return `
                <option value="MGD">MGD</option>
                <option value="m3/d">m³/d</option>
            `
    }
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
