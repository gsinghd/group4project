
const stateAbbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
};

// Reverse the mapping for easier lookup
const stateNames = {};
for (let fullName in stateAbbreviations) {
    stateNames[stateAbbreviations[fullName]] = fullName;
}

let currentLayer = null; // Variable to store the current layer

function initMap() {
    map = L.map('map').setView([37.8, -96], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    document.getElementById('industryGrowthBtn').addEventListener('click', () => {
        loadGrowthData('/state-industry-growth-data');
    });

    document.getElementById('regionalGrowthBtn').addEventListener('click', () => {
        loadGrowthData('/state-regional-growth-data');
    });
}

function loadGrowthData(url) {
    if (currentLayer) {
        map.removeLayer(currentLayer); // Remove the existing layer if present
    }

    fetch('/static/data/statesData.geojson')
        .then(response => response.json())
        .then(geojsonData => {
            fetch(url)
                .then(response => response.json())
                .then(growthData => {
                    console.log("Growth Data:", growthData);
                    console.log("State Names Mapping:", stateNames);

                    currentLayer = L.geoJson(geojsonData, {
                        style: feature => {
                            let fullStateName = feature.properties.name;  // Full state name from GeoJSON
                            let stateAbbr = stateAbbreviations[fullStateName];  // Convert full name to abbreviation
                            let growth = growthData[stateAbbr];  // Use abbreviation to access data

                            console.log(fullStateName, stateAbbr, growth);  // Log to verify correct mapping and data retrieval

                            return {
                                fillColor: getColor(growth),
                                weight: 2,
                                opacity: 1,
                                color: 'white',
                                dashArray: '3',
                                fillOpacity: 0.7
                            };
                        },
                        onEachFeature: (feature, layer) => {
                            let fullStateName = feature.properties.name;
                            let stateAbbr = stateAbbreviations[fullStateName];
                            let growth = growthData[stateAbbr];
                            let growthPercentage = growth ? (growth * 100).toFixed(2) + '%' : 'No data';
                            let popupContent = `${fullStateName}: ${growthPercentage}`;
                            layer.bindPopup(popupContent);
                            layer.on({
                                mouseover: (e) => {
                                    let layer = e.target;
                                    layer.openPopup();
                                    layer.setStyle({
                                        weight: 5,
                                        color: '#666',
                                        dashArray: '',
                                        fillOpacity: 0.7
                                    });
                                },
                                mouseout: (e) => {
                                    let layer = e.target;
                                    layer.closePopup();
                                    layer.setStyle({
                                        weight: 2,
                                        color: 'white',
                                        dashArray: '3',
                                        fillOpacity: 0.7
                                    });
                                }
                            });
                        }
                    }).addTo(map);
                });
        })
        .catch(error => console.error('Error:', error));
}

function getColor(growth) {
    if (growth === undefined || isNaN(growth)) return '#808080'; // Return grey if no data or invalid data
    const value = parseFloat(growth) * 100; // Convert to percentage
    const red = value < 0 ? 255 * Math.min(1, -value / 100) : 0;
    const green = value > 0 ? 255 * Math.min(1, value / 100) : 0;
    return `rgb(${Math.round(red)},${Math.round(green)},0)`;
}

document.addEventListener('DOMContentLoaded', initMap);
