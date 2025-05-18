// Custom search functionality that can handle any input
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const searchResults = document.getElementById('searchResults');
    
    // Override the search button click handler
    if (searchButton) {
        searchButton.addEventListener('click', customSearch);
    }
    
    // Override the search input keyup handler
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                customSearch();
            }
        });
    }
    
    // Custom search function that can handle any input
    function customSearch() {
        const query = searchInput.value.trim();
        
        if (query === '') {
            searchResults.innerHTML = '<div class="no-results">Enter a search term</div>';
            return;
        }
        
        // Show searching indicator
        searchResults.innerHTML = '<div class="no-results">Searching...</div>';
        
        // Try to search in wealthy individuals data first
        if (typeof searchWealthyIndividuals === 'function') {
            const foundInWealthyData = searchWealthyIndividuals(query);
            
            if (foundInWealthyData) {
                return;
            }
        }
        
        // If not found in wealthy data, try to search by location
        if (typeof markersGroup !== 'undefined') {
            markersGroup.clearLayers();
        }
        
        // Use the Zillow API to search for properties
        searchByZillowAPI(query);
    }
    
    // Function to search using Zillow API
    function searchByZillowAPI(query) {
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
                    
                    // If geocoding fails, try alternative search methods
                    tryAlternativeSearch(query);
                } catch (e) {
                    console.error('Failed to parse geocoding data', e);
                    // If geocoding fails, try alternative search methods
                    tryAlternativeSearch(query);
                }
            }
        });
        
        geocodeXhr.open('GET', `https://maps-data.p.rapidapi.com/geocoding.php?query=${encodeURIComponent(query)}&lang=en&country=us`);
        geocodeXhr.setRequestHeader('x-rapidapi-key', '39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75');
        geocodeXhr.setRequestHeader('x-rapidapi-host', 'maps-data.p.rapidapi.com');
        
        geocodeXhr.send();
    }
    
    // Function to search properties by coordinates using Zillow API
    function searchPropertiesByCoordinates(lat, lng, radius = 0.5) {
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
                        if (typeof markersGroup !== 'undefined') {
                            markersGroup.clearLayers();
                        }
                        
                        // Display search results
                        searchResults.innerHTML = `<div class="result-item">
                            <div style="font-weight: 600; font-size: 18px;">Properties near (${lat.toFixed(4)}, ${lng.toFixed(4)})</div>
                            <div style="color: #666;">${response.results.length} properties found</div>
                        </div>`;
                        
                        // Add markers for each property
                        response.results.forEach(property => {
                            if (property.latitude && property.longitude && typeof L !== 'undefined' && typeof markersGroup !== 'undefined') {
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
                        if (typeof L !== 'undefined' && typeof markersGroup !== 'undefined') {
                            L.circle([lat, lng], radius * 1609.34).addTo(markersGroup); // Convert miles to meters
                        }
                        
                        // Fit map to show all markers
                        if (response.results.length > 0 && typeof L !== 'undefined' && typeof map !== 'undefined') {
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
    }
    
    // Function to try alternative search methods when geocoding fails
    function tryAlternativeSearch(query) {
        // Show no results found with helpful suggestions
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
    }
});