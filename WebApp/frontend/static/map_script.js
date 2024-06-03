var map;

function initMap() {
    map = L.map('map').setView([37.8, -96], 4); // Center on the US

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    fetch('/static/data/statesData.geojson')  // Ensure the file path is correct
        .then(response => response.json())
        .then(geojsonData => {
            fetch('/growth-data')
                .then(response => response.json())
                .then(growthData => {
                    L.geoJson(geojsonData, {
                        style: feature => ({
                            fillColor: getColor(growthData[feature.properties.name]),
                            weight: 2,
                            opacity: 1,
                            color: 'white',
                            dashArray: '3',
                            fillOpacity: 0.7
                        })
                    }).addTo(map);
                });
        });
}

function getColor(growth) {
    return growth > 0 ? '#31a354' : // green for positive growth
           growth < 0 ? '#de2d26' : // red for decline
                       '#ffcc00';   // yellow for neutral
}

document.addEventListener('DOMContentLoaded', initMap);
