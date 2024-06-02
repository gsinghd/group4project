// script.js
var map;

function initMap() {
    // Initialize the map
    map = L.map('map').setView([39.8283, -98.5795], 4);

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

function setStateLocation(){
    var selectElement = document.getElementById('stateSelect');
    var selectedState = selectElement.value;
    fetch("/state_location/" + selectedState)
        .then(response => response.json())
        .then(data => {
            map.eachLayer(function (layer) {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });
            var marker = L.marker([data.latitude, data.longitude]).addTo(map);
            marker.bindPopup("<b>" + selectedState + "</b><br>Latitude: " + data.latitude + "<br>Longitude: " + data.longitude).openPopup();
            map.setView([ data.latitude, data.longitude], 6);
        })
        .catch(error => console.error('Error:', error));
}

function populateData() {
    var dataContainer = document.getElementById('dataResponse');

    var selectElement = document.getElementById('datasetSelect');
    var selectedDataset = selectElement.value;
    var url = ""
    if (selectedDataset.includes('type')) {
        var selectElement = document.getElementById('stateSelect');
        var selectedState = selectElement.value;
        var selectElement = document.getElementById('typeSelect');
        var selectedType = selectElement.value;
        url = "/type_data/" + selectedDataset + "/" + selectedState + "/" + selectedType
    } else if (selectedDataset.includes('state')) {
        var selectElement = document.getElementById('stateSelect');
        var selectedState = selectElement.value;
        url = "/state_data/" + selectedDataset + "/" + selectedState
    } else {
        var selectElement = document.getElementById('regionSelect');
        var selectedRegion = selectElement.value;
        url = "/region_data/" + selectedDataset + "/" + selectedRegion
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            dataContainer.textContent = selectedDataset + ": " + data;
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

    if (selectedDataset.includes('type')) {
        fetch(`/types/${selectedDataset}`)
            .then(response => response.json())
            .then((types) => {
                types.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type;
                    option.text = type;
                    typeSelect.add(option);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    if (selectedDataset.includes('state')) {
        fetch(`/states/${selectedDataset}`)
            .then(response => response.json())
            .then((states) => {
                states.forEach(state => {
                    const option = document.createElement('option');
                    option.value = state;
                    option.text = state;
                    stateSelect.add(option);
                });
            })
            .catch(error => console.error('Error:', error));
    } else {
        fetch(`/regions/${selectedDataset}`)
            .then(response => response.json())
            .then((regions) => {
                regions.forEach(region => {
                    const option = document.createElement('option');
                    option.value = region;
                    option.text = region;
                    regionSelect.add(option);
                });
            })
            .catch(error => console.error('Error:', error));

    }
    // Fetch states and regions for the selected dataset
    // Promise.all([
    //     fetch(`/states/${selectedDataset}`),
    //     fetch(`/regions/${selectedDataset}`)
    // ])
    // .then(responses => Promise.all(responses.map(response => response.json())))
    // .then(([states, regions]) => {
    //     states.forEach(state => {
    //         const option = document.createElement('option');
    //         option.value = state;
    //         option.text = state;
    //         stateSelect.add(option);
    //     });

    //     regions.forEach(region => {
    //         const option = document.createElement('option');
    //         option.value = region;
    //         option.text = region;
    //         regionSelect.add(option);
    //     });
    // })
    // .catch(error => console.error('Error:', error));
}
populateStateRegionSelect();

// Event listener for dataset selection
datasetSelect.addEventListener('change', () => {
    populateStateRegionSelect();
    fetchData();
});

// Event listener for state selection
stateSelect.addEventListener('change', () => {
    fetchData();
    setStateLocation();
});

function fetchData() {
    const selectedDataset = datasetSelect.value;
    const selectedState = stateSelect.value;

    fetch(`/data/${selectedDataset}/${selectedState}`)
        .then(response => response.json())
        .then(data => {
            // Update the UI with the fetched data
            const dataContainer = document.getElementById('data-container');
            // Clear previous content
            dataContainer.innerHTML = '';
            // Create elements to display the fetched data
            const dataList = document.createElement('ul');
            data.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = item.property; // Adjust this based on your data structure
                dataList.appendChild(listItem);
            });
            // Append the list to the data container
            dataContainer.appendChild(dataList);
        })
        .catch(error => console.error('Error fetching data:', error));
}
