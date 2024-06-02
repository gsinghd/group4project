// script.js
function initMap() {
    // Initialize the map
    var map = L.map('map').setView([39.8283, -98.5795], 4);

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

function populateStateRegionSelect() {
    const datasetSelect = document.getElementById('datasetSelect');
    const stateSelect = document.getElementById('stateSelect');
    const regionSelect = document.getElementById('regionSelect');

    // Clear previous options
    stateSelect.innerHTML = '<option value="" disabled selected>Select a state</option>';
    regionSelect.innerHTML = '<option value="" disabled selected>Select a region</option>';

    const selectedDataset = datasetSelect.value;

    // Fetch states for the selected dataset
    fetch(`/states/${selectedDataset}`)
        .then(response => response.json())
        .then(states => {
            states.forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.text = state;
                stateSelect.add(option);
            });
        })
        .catch(error => console.error('Error:', error));

    // Fetch regions for the selected dataset
    fetch(`/regions/${selectedDataset}`)
        .then(response => response.json())
        .then(regions => {
            regions.forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.text = region;
                regionSelect.add(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Event listener for dataset selection
datasetSelect.addEventListener('change', populateStateRegionSelect);

