// Data sources and loading functions for the Wealth Map Platform

// Global variable to store wealthy individuals data
let wealthyIndividualsData = null;

// Function to load wealthy individuals data
function loadWealthyIndividualsData() {
    return fetch(CONFIG.dataSources.wealthyIndividuals)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load wealthy individuals data');
            }
            return response.json();
        })
        .then(data => {
            wealthyIndividualsData = data;
            console.log('Wealthy individuals data loaded:', data);
            return data;
        })
        .catch(error => {
            console.error('Error loading wealthy individuals data:', error);
            return null;
        });
}

// Function to search wealthy individuals data
function searchWealthyIndividuals(query) {
    if (!wealthyIndividualsData) {
        console.warn('Wealthy individuals data not loaded yet');
        return false;
    }
    
    query = query.toLowerCase();
    let results = [];
    
    // Search through wealthy individuals
    wealthyIndividualsData.wealthyIndividuals.forEach(individual => {
        // Check if name matches
        if (individual.name.toLowerCase().includes(query)) {
            results.push({
                type: 'individual',
                name: individual.name,
                netWorth: individual.netWorth,
                propertyCount: individual.properties.length,
                properties: individual.properties
            });
        } else {
            // Check if any property address matches
            individual.properties.forEach(property => {
                if (property.address.toLowerCase().includes(query)) {
                    results.push({
                        type: 'property',
                        address: property.address,
                        owner: individual.name,
                        value: property.value,
                        coordinates: property.coordinates,
                        details: property
                    });
                }
            });
        }
    });
    
    if (results.length > 0) {
        displayWealthySearchResults(results, query);
        return true;
    }
    
    return false;
}

// Function to display wealthy individuals search results
function displayWealthySearchResults(results, query) {
    const searchResults = document.getElementById('searchResults');
    
    // Clear existing markers
    if (typeof markersGroup !== 'undefined') {
        markersGroup.clearLayers();
    }
    
    // Display search results
    let resultsHTML = '';
    
    results.forEach(result => {
        if (result.type === 'individual') {
            resultsHTML += `
                <div class="result-item" data-type="individual" data-name="${result.name}">
                    <div style="font-weight: 600; font-size: 18px;">${result.name}</div>
                    <div style="color: #666;">Net Worth: ${result.netWorth} | ${result.propertyCount} properties</div>
                </div>
            `;
            
            // Add markers for all properties of this individual
            result.properties.forEach(property => {
                addPropertyMarker(property, result.name);
            });
            
        } else if (result.type === 'property') {
            resultsHTML += `
                <div class="result-item" data-type="property" data-lat="${result.coordinates[0]}" data-lng="${result.coordinates[1]}">
                    <div style="font-weight: 600; font-size: 18px;">${result.address}</div>
                    <div style="color: #666;">Owner: ${result.owner} | Value: ${result.value}</div>
                </div>
            `;
            
            // Add marker for this property
            addPropertyMarker(result.details, result.owner);
        }
    });
    
    searchResults.innerHTML = resultsHTML;
    
    // Add click event listeners to result items
    document.querySelectorAll('.result-item').forEach(item => {
        item.addEventListener('click', function() {
            const type = this.getAttribute('data-type');
            
            if (type === 'property') {
                const lat = parseFloat(this.getAttribute('data-lat'));
                const lng = parseFloat(this.getAttribute('data-lng'));
                
                // Center map on property
                if (typeof map !== 'undefined') {
                    map.setView([lat, lng], 16);
                }
            } else if (type === 'individual') {
                const name = this.getAttribute('data-name');
                const individual = wealthyIndividualsData.wealthyIndividuals.find(i => i.name === name);
                
                if (individual && individual.properties.length > 0) {
                    // Create bounds for all properties
                    const bounds = L.latLngBounds(individual.properties.map(p => p.coordinates));
                    
                    // Fit map to show all properties
                    if (typeof map !== 'undefined') {
                        map.fitBounds(bounds, { padding: [50, 50] });
                    }
                }
            }
        });
    });
    
    // Fit map to show all markers
    if (typeof map !== 'undefined' && typeof markersGroup !== 'undefined') {
        const bounds = markersGroup.getBounds();
        if (bounds.isValid()) {
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    }
}

// Function to add a property marker to the map
function addPropertyMarker(property, ownerName) {
    if (!property.coordinates || typeof L === 'undefined' || typeof markersGroup === 'undefined') {
        return;
    }
    
    const marker = L.marker(property.coordinates).addTo(markersGroup);
    
    let popupContent = `
        <div style="min-width: 200px;">
            <h3 style="margin: 0 0 5px 0;">${property.address}</h3>
            <p style="margin: 0 0 5px 0;"><strong>Owner:</strong> ${ownerName}</p>
    `;
    
    if (property.value) {
        popupContent += `<p style="margin: 0 0 5px 0;"><strong>Value:</strong> ${property.value}</p>`;
    }
    
    if (property.bedrooms) {
        popupContent += `<p style="margin: 0 0 5px 0;"><strong>Beds:</strong> ${property.bedrooms}</p>`;
    }
    
    if (property.bathrooms) {
        popupContent += `<p style="margin: 0 0 5px 0;"><strong>Baths:</strong> ${property.bathrooms}</p>`;
    }
    
    if (property.squareFootage) {
        popupContent += `<p style="margin: 0 0 5px 0;"><strong>Size:</strong> ${property.squareFootage.toLocaleString()} sq ft</p>`;
    }
    
    if (property.description) {
        popupContent += `<p style="margin: 0 0 5px 0;"><strong>Description:</strong> ${property.description}</p>`;
    }
    
    popupContent += `
        <button class="view-details-btn" style="background-color: #3498db; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-top: 5px;" 
            onclick="showPropertyDetails('${property.address.replace(/'/g, "\\'")}', ${JSON.stringify(property).replace(/"/g, '&quot;')}, '${ownerName.replace(/'/g, "\\'")}')">
            View Full Details
        </button>
    </div>`;
    
    marker.bindPopup(popupContent);
    
    return marker;
}

// Function to show property details panel
function showPropertyDetails(address, property, ownerName) {
    const detailsPanel = document.getElementById('property-details');
    
    // Set property address
    document.getElementById('property-address').textContent = address;
    
    // Set basic info
    document.getElementById('property-type').textContent = 'Residential';
    document.getElementById('year-built').textContent = property.history ? property.history[0].year : 'Unknown';
    document.getElementById('square-footage').textContent = property.squareFootage ? `${property.squareFootage.toLocaleString()} sq ft` : 'Unknown';
    document.getElementById('lot-size').textContent = property.lotSize || 'Unknown';
    document.getElementById('bedrooms').textContent = property.bedrooms || 'Unknown';
    document.getElementById('bathrooms').textContent = property.bathrooms || 'Unknown';
    
    // Set ownership info
    document.getElementById('current-owner').textContent = ownerName;
    document.getElementById('owner-since').textContent = property.history ? `Since ${property.history[0].year}` : 'Unknown';
    document.getElementById('owner-type').textContent = 'Individual';
    document.getElementById('mailing-address').textContent = 'Same as property';
    document.getElementById('related-properties').textContent = 'Information not available';
    
    // Set financial info
    document.getElementById('current-value').textContent = property.value || 'Unknown';
    document.getElementById('last-sale-price').textContent = property.history ? property.history[0].value : 'Unknown';
    document.getElementById('last-sale-date').textContent = property.history ? `${property.history[0].year}` : 'Unknown';
    document.getElementById('property-taxes').textContent = 'Information not available';
    document.getElementById('tax-assessment').textContent = 'Information not available';
    document.getElementById('mortgage-info').textContent = 'Information not available';
    
    // Set history info (timeline)
    if (property.history && property.history.length > 0) {
        let timelineHTML = '';
        
        property.history.forEach(historyItem => {
            timelineHTML += `
                <div class="timeline-item">
                    <div class="timeline-date">${historyItem.year}</div>
                    <div class="timeline-content">
                        <h4>Property Valuation</h4>
                        <p>Valued at ${historyItem.value}</p>
                    </div>
                </div>
            `;
        });
        
        document.getElementById('history').innerHTML = `<div class="timeline">${timelineHTML}</div>`;
    } else {
        document.getElementById('history').innerHTML = '<div class="no-results">No historical data available</div>';
    }
    
    // Show the details panel
    detailsPanel.classList.add('active');
}

// Function to geocode a location query
function geocodeLocation(query) {
    // First try to geocode the query to get coordinates
    const geocodeXhr = new XMLHttpRequest();
    geocodeXhr.withCredentials = true;
    
    geocodeXhr.addEventListener('readystatechange', function() {
        if (this.readyState === this.DONE) {
            try {
                const response = JSON.parse(this.responseText);
                console.log('Geocoding result:', response);
                
                // If valid coordinates are returned, search properties by coordinates
                if (response && response.data && response.data.length > 0) {
                    const location = response.data[0];
                    if (location.lat && location.lng) {
                        // Update search results
                        searchResults.innerHTML = `<div class="result-item">
                            <div style="font-weight: 600; font-size: 18px;">${location.name || query}</div>
                            <div style="color: #666;">Location found - Searching for properties...</div>
                        </div>`;
                        
                        // Search for properties using the coordinates
                        searchPropertiesByCoordinates(location.lat, location.lng, 0.5);
                        return;
                    }
                }
                
                // If geocoding fails, show no results
                searchResults.innerHTML = `<div class="no-results">
                    <p>No matching results found for "${query}"</p>
                    <p>Try searching for:</p>
                    <ul style="padding-left: 20px; margin-top: 5px;">
                        <li>Owner names (e.g., "Elon Musk")</li>
                        <li>Locations (e.g., "Beverly Hills")</li>
                        <li>Property features (e.g., "waterfront", "mansion")</li>
                        <li>Bedroom/bathroom counts (e.g., "5 bedroom")</li>
                    </ul>
                </div>`;
            } catch (e) {
                console.error('Failed to parse geocoding data', e);
                // If geocoding fails, show error
                searchResults.innerHTML = '<div class="no-results">Error searching for location</div>';
            }
        }
    });
    
    geocodeXhr.open('GET', `https://maps-data.p.rapidapi.com/geocoding.php?query=${encodeURIComponent(query)}&lang=en&country=us`);
    geocodeXhr.setRequestHeader('x-rapidapi-key', 'YOUR_RAPIDAPI_KEY');
    geocodeXhr.setRequestHeader('x-rapidapi-host', 'maps-data.p.rapidapi.com');
    
    geocodeXhr.send();
}