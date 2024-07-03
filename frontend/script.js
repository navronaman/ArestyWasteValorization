// load sidebar/navbar
document.addEventListener('DOMContentLoaded', function() {
    // Fetch the navbar
    fetch('assets\\navbar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar-placeholder').innerHTML = data;
        });

    fetch('assets\\unitbutton.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('unitbutton-placeholder').innerHTML = data;
        });

    fetch('assets\\njname.svg')
        .then(response => response.text())
        .then(data => {
            document.getElementById('mapContainer').innerHTML = data;
            attachEventListenersToMap();
    });
    fetch('assets\\exportcsv.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('export-container').innerHTML = data;
    });
}); 


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

var currentCounty = null; // current county selected
var previousCounty = null; // previous county selected (for comparison)

var currentCountyData = null; // current county data
var previousCountyData = null; // previous county data (for comparison)

// imperial/metric button
var unit = null;
function selectUnit(imperial_or_metric) {
    console.log(imperial_or_metric);

    // implement the changeSettings function to change the units in all of HTML
    if (imperial_or_metric == "imperial") {
        unit = "imperial";
        changeSettings(unit);
    }
    else if (imperial_or_metric == "metric") {
        unit = "metric";
        changeSettings(unit);
    }
    
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
    }} 
/*

Most important of code
-It changes the color of the county when the mouse hovers over it
-It also displays the county name when the mouse hovers over it
-It displays the county information when the county is clicked

*/
// load map

function attachEventListenersToMap() {
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
}

// Collapsible content
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.collapsible-header');
    const container = document.querySelector('.collapsible-container');

    header.addEventListener('click', () => {
        container.classList.toggle('active');
    });


});