// script.js
function initMap() {
    // Initialize the map
    var map = L.map('map').setView([33.9806, -117.3755], 13);

    // Add the OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

function populateDatasetSelect() {
    const datasetSelect = document.getElementById('datasetSelect');

    fetch('/datasets')
        .then(response => response.json())
        .then(datasets => {
            datasets.forEach(dataset => {
                const option = document.createElement('option');
                option.value = dataset;
                option.text = dataset;
                datasetSelect.add(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Call the function to populate the dataset select on page load
populateDatasetSelect();


