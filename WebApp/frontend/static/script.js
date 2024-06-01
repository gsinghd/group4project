// script.js
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener("DOMContentLoaded", function() {
        // Initialize the map and set its view
        var map = L.map('map').setView([51.505, -0.09], 13); // Example coordinates (London)
    
        // Add the OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);
    
        // Example marker
        L.marker([51.505, -0.09]).addTo(map)
            .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
            .openPopup();
    });
    
    //fetchData();
});

function fetchData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            const dataContainer = document.getElementById('data-container');
            dataContainer.innerHTML = ''; // Clear previous data

            data.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.textContent = `ID: ${item.id}, Name: ${item.name}`;
                dataContainer.appendChild(itemElement);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}
