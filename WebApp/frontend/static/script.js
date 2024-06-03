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

const tableDisplayNames = {
    "average_list_price_by_region": "Average List Price by Region",
    "average_list_price_by_state": "Average List Price by State",
    "average_sale_price_by_region": "Average Sale Price by Region",
    "average_sale_price_by_state": "Average Sale Price by State",
    "avg_price_change_by_state": "Average Price Change by State",
    "avg_price_change_region": "Average Price Change by Region",
    "median_dom_state_by_type": "Median Days on Market by State and Property Type",
    "median_prices_state_prop_type": "Median Prices by State and Property Type"
};

const excludedDatasets = [
    "industry_potential_by_region",
    "regional_growth_by_region",
    "temp_table"
];

function openMapPage() {
    window.open('/us-map', '_blank');
}

function populateDatasetSelect() {
    const datasetSelect = document.getElementById('datasetSelect');

    fetch('/datasets')
        .then(response => response.json())
        .then(datasets => {
            datasets.forEach(dataset => {
                if (!excludedDatasets.includes(dataset)) {
                    const displayName = tableDisplayNames[dataset] || dataset;
                    const option = document.createElement('option');
                    option.value = dataset;
                    option.text = displayName;
                    datasetSelect.add(option);
                }
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

function setRegionLocation(){
    var selectElement = document.getElementById('regionSelect');
    var selectedRegion = selectElement.value.slice(-5);
    fetch("/region_location/" + selectedRegion)
        .then(response => response.json())
        .then(data => {
            console.log(data.lat)
            map.eachLayer(function (layer) {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });
            var marker = L.marker([data.lat, data.lng]).addTo(map);
            marker.bindPopup("<b>" + selectedRegion + "</b><br>Latitude: " + data.lat + "<br>Longitude: " + data.lng).openPopup();
            map.setView([ data.lat, data.lng], 6);
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
            var datasetLabel = getDatasetLabel(selectedDataset);
            var price = data[0];
            dataContainer.innerHTML = "<h3>" + datasetLabel + "</h3>" + price;
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
    typeSelect.innerHTML = '<option value="" disabled selected>Select a property type</option>';

    const selectedDataset = datasetSelect.value;

    if (selectedDataset.includes('type')) {
        fetch(`/types/${selectedDataset}`)
            .then(response => response.json())
            .then((types) => {
                types.forEach(type => {
                    console.log("Fetched types:", types);
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
}

function getDatasetLabel(dataset) {
    // Customize the label based on the dataset type or any other criteria
    if (dataset.includes('average_sale_price_by_region')) {
        return "Average Sale Price by Region: ";
    } else if (dataset.includes('average_sale_price_by_state')) {
        return "Average Sale Price by State: ";
    } else if (dataset.includes('average_list_price_by_region')) {
        return "Average List Price By Region: ";
    } else if(dataset.includes('average_list_price_by_state')){
        return "Average List Price By State: ";
    } else if(dataset.includes('avg_price_change_by_state')){
        return "Average Price Change By State: ";
    } else if(dataset.includes('avg_price_change_region')){
        return "Average Price Change By Region: ";
    } else if(dataset.includes('property_stats')){
        return "Property Statistics: ";
    } else if (dataset.includes('median_dom_state_by_type')){
        return "Median Days on Market By State and Property Type";
    } else if(dataset.includes('median_prices_state_prop')){
        return "Median Prices By State and Property Type";
    }else {
        return "Data for " + dataset;
    }
}
populateStateRegionSelect();

const datasetSelect = document.getElementById('datasetSelect');
const stateSelect = document.getElementById('stateSelect');
const regionSelect = document.getElementById('regionSelect');
const navigateButton = document.getElementById('navigateButton');

// Event listener for dataset selection
datasetSelect.addEventListener('change', () => {
    populateStateRegionSelect();
    fetchData();
});

// Event listener for region selection
regionSelect.addEventListener('change', () => {
    setRegionLocation();
});

// Event listener for state selection
stateSelect.addEventListener('change', () => {
    fetchData();
    setStateLocation();
});

navigateButton.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/us-map';
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
