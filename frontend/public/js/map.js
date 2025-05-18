// Map initialization and functionality for the Wealth Map Platform

// Global variables
let map;
let markersGroup;

// Initialize the map
function initMap() {
    // Create the map
    map = L.map('map', {
        center: CONFIG.map.center,
        zoom: CONFIG.map.zoom,
        minZoom: CONFIG.map.minZoom,
        maxZoom: CONFIG.map.maxZoom
    });
    
    // Add the tile layer
    L.tileLayer(CONFIG.map.tileLayer, {
        attribution: CONFIG.map.attribution
    }).addTo(map);
    
    // Create a layer group for markers
    markersGroup = L.layerGroup().addTo(map);
    
    // Add event listeners
    map.on('click', onMapClick);
    
    console.log('Map initialized');
}

// Handle map click event
function onMapClick(e) {
    console.log('Map clicked at:', e.latlng);
    
    // Close the property details panel if it's open
    const detailsPanel = document.getElementById('property-details');
    if (detailsPanel.classList.contains('active')) {
        detailsPanel.classList.remove('active');
    }
}

// Function to add property markers to the map
function addPropertyMarkers(properties) {
    // Clear existing markers
    markersGroup.clearLayers();
    
    // Add new markers
    properties.forEach(property => {
        if (property.coordinates) {
            const marker = L.marker(property.coordinates).addTo(markersGroup);
            
            let popupContent = `
                <div style="min-width: 200px;">
                    <h3 style="margin: 0 0 5px 0;">${property.address || 'Property'}</h3>
            `;
            
            if (property.owner) {
                popupContent += `<p style="margin: 0 0 5px 0;"><strong>Owner:</strong> ${property.owner}</p>`;
            }
            
            if (property.value) {
                popupContent += `<p style="margin: 0 0 5px 0;"><strong>Value:</strong> ${property.value}</p>`;
            }
            
            if (property.bedrooms) {
                popupContent += `<p style="margin: 0 0 5px 0;"><strong>Beds:</strong> ${property.bedrooms}</p>`;
            }
            
            if (property.bathrooms) {
                popupContent += `<p style="margin: 0 0 5px 0;"><strong>Baths:</strong> ${property.bathrooms}</p>`;
            }
            
            popupContent += `
                <button class="view-details-btn" style="background-color: #3498db; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-top: 5px;" 
                    onclick="showPropertyDetails('${property.address?.replace(/'/g, "\\'")}', ${JSON.stringify(property).replace(/"/g, '&quot;')}, '${property.owner?.replace(/'/g, "\\'")}')">
                    View Full Details
                </button>
            </div>`;
            
            marker.bindPopup(popupContent);
        }
    });
    
    // Fit map to show all markers if there are any
    if (markersGroup.getLayers().length > 0) {
        map.fitBounds(markersGroup.getBounds(), { padding: [50, 50] });
    }
}

// Function to add a boundary polygon to the map
function addPropertyBoundary(property) {
    if (!property.boundaries) {
        return null;
    }
    
    const { northLat, southLat, eastLng, westLng } = property.boundaries;
    
    const bounds = [
        [northLat, westLng],
        [northLat, eastLng],
        [southLat, eastLng],
        [southLat, westLng]
    ];
    
    const polygon = L.polygon(bounds, {
        color: '#e74c3c',
        weight: 2,
        fillColor: '#e74c3c',
        fillOpacity: 0.2
    }).addTo(markersGroup);
    
    return polygon;
}

// Function to search properties by coordinates
function searchPropertiesByCoordinates(lat, lng, radius = 0.5) {
    console.log(`Searching for properties near (${lat}, ${lng}) with radius ${radius} miles`);
    
    // This would normally be an API call, but for demo purposes we'll just show a message
    const searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = `<div class="result-item">
        <div style="font-weight: 600; font-size: 18px;">Properties near (${lat.toFixed(4)}, ${lng.toFixed(4)})</div>
        <div style="color: #666;">Searching for properties...</div>
    </div>`;
    
    // Clear existing markers
    markersGroup.clearLayers();
    
    // Add a marker at the search location
    const marker = L.marker([lat, lng]).addTo(markersGroup);
    marker.bindPopup(`<div>Search Location</div>`).openPopup();
    
    // Add a circle to show the search radius
    L.circle([lat, lng], radius * 1609.34).addTo(markersGroup); // Convert miles to meters
    
    // Center the map on the search location
    map.setView([lat, lng], 14);
    
    // In a real application, we would make an API call here to get properties
    // For now, we'll just show a message after a delay to simulate an API call
    setTimeout(() => {
        searchResults.innerHTML = `<div class="no-results">
            <p>This is a demo application. In a real application, this would show properties near (${lat.toFixed(4)}, ${lng.toFixed(4)}).</p>
            <p>Try searching for one of these wealthy individuals instead:</p>
            <ul style="padding-left: 20px; margin-top: 5px;">
                <li>Elon Musk</li>
                <li>Jeff Bezos</li>
                <li>Bill Gates</li>
                <li>Mark Zuckerberg</li>
                <li>Warren Buffett</li>
            </ul>
        </div>`;
    }, 1500);
}