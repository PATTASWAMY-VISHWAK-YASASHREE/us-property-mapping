// This script updates the searchPropertiesByCoordinates function with the new Zillow API integration

// Wait for the document to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Override the searchPropertiesByCoordinates function if it exists
    if (typeof window.searchPropertiesByCoordinates === 'function') {
        window.searchPropertiesByCoordinates = function(lat, lng, radius = 0.5) {
            const data = null;
            const xhr = new XMLHttpRequest();
            xhr.withCredentials = true;

            xhr.addEventListener('readystatechange', function () {
                if (this.readyState === this.DONE) {
                    try {
                        const response = JSON.parse(this.responseText);
                        console.log('Properties by coordinates:', response);
                        
                        if (response && response.results && response.results.length > 0) {
                            // Clear existing markers
                            markersGroup.clearLayers();
                            
                            // Display search results
                            searchResults.innerHTML = `<div class="result-item">
                                <div style="font-weight: 600; font-size: 18px;">Properties near (${lat.toFixed(4)}, ${lng.toFixed(4)})</div>
                                <div style="color: #666;">${response.results.length} properties found</div>
                            </div>`;
                            
                            // Add markers for each property
                            response.results.forEach(property => {
                                if (property.latitude && property.longitude) {
                                    const marker = L.marker([property.latitude, property.longitude]).addTo(markersGroup);
                                    
                                    let popupContent = `
                                        <div style="min-width: 200px;">
                                            <h3 style="margin: 0 0 5px 0;">${property.address || 'Property'}</h3>
                                    `;
                                    
                                    if (property.price) {
                                        popupContent += `<p style="margin: 0 0 5px 0;"><strong>Price:</strong> ${property.price}</p>`;
                                    }
                                    
                                    if (property.bedrooms) {
                                        popupContent += `<p style="margin: 0 0 5px 0;"><strong>Beds:</strong> ${property.bedrooms}</p>`;
                                    }
                                    
                                    if (property.bathrooms) {
                                        popupContent += `<p style="margin: 0 0 5px 0;"><strong>Baths:</strong> ${property.bathrooms}</p>`;
                                    }
                                    
                                    if (property.zpid) {
                                        popupContent += `<p style="margin: 0 0 5px 0;"><strong>ZPID:</strong> ${property.zpid}</p>`;
                                    }
                                    
                                    popupContent += `</div>`;
                                    
                                    marker.bindPopup(popupContent);
                                }
                            });
                            
                            // Add a circle to show the search radius
                            L.circle([lat, lng], radius * 1609.34).addTo(markersGroup); // Convert miles to meters
                            
                            // Fit map to show all markers
                            if (response.results.length > 0) {
                                const bounds = L.latLngBounds(
                                    response.results
                                        .filter(p => p.latitude && p.longitude)
                                        .map(p => [p.latitude, p.longitude])
                                );
                                map.fitBounds(bounds, { padding: [50, 50] });
                            }
                        } else {
                            searchResults.innerHTML = '<div class="no-results">No properties found in this area</div>';
                        }
                    } catch (e) {
                        console.error('Failed to parse property search results', e);
                        searchResults.innerHTML = '<div class="no-results">Error searching for properties</div>';
                    }
                }
            });

            // Updated API endpoint with more parameters for flexible searching
            xhr.open('GET', `https://zillow-working-api.p.rapidapi.com/search/bycoordinates?latitude=${lat}&longitude=${lng}&radius=${radius}&page=1&sortOrder=Homes_for_you&listingStatus=For_Sale&bed_min=No_Min&bed_max=No_Max&bathrooms=Any&homeType=Houses%2C%20Townhomes%2C%20Multi-family%2C%20Condos%2FCo-ops%2C%20Lots-Land%2C%20Apartments%2C%20Manufactured&maxHOA=Any&listingType=By_Agent&listingTypeOptions=Agent%20listed%2CNew%20Construction%2CFore-closures%2CAuctions&parkingSpots=Any&daysOnZillow=Any&soldInLast=Any`);
            xhr.setRequestHeader('x-rapidapi-key', '39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75');
            xhr.setRequestHeader('x-rapidapi-host', 'zillow-working-api.p.rapidapi.com');

            xhr.send(data);
        };
    }

    // Enhance the search functionality to handle any input
    if (typeof window.performSearch === 'function') {
        const originalPerformSearch = window.performSearch;
        
        window.performSearch = function() {
            const query = searchInput.value.trim();
            
            if (query === '') {
                searchResults.innerHTML = '<div class="no-results">Enter a search term</div>';
                return;
            }
            
            // Show searching indicator
            searchResults.innerHTML = '<div class="no-results">Searching...</div>';
            
            // Try to search in our wealthy individuals data first
            const foundInWealthyData = searchWealthyIndividuals(query);
            
            if (!foundInWealthyData) {
                // If not found in our data, try geocoding the search term
                markersGroup.clearLayers();
                
                // Show searching for location message
                searchResults.innerHTML = '<div class="no-results">Searching for location or other matches...</div>';
                
                // Try to geocode the location
                geocodeLocation(query);
            }
        };
    }
});