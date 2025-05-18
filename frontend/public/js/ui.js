// UI functionality for the Wealth Map Platform

// Initialize UI elements and event listeners
function initUI() {
    // Get DOM elements
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const propertyValueSlider = document.getElementById('property-value-slider');
    const propertyValueDisplay = document.getElementById('property-value-display');
    const yearBuiltSlider = document.getElementById('year-built-slider');
    const yearBuiltDisplay = document.getElementById('year-built-display');
    const applyFiltersButton = document.getElementById('apply-filters');
    const closeDetailsButton = document.getElementById('close-details');
    const tabButtons = document.querySelectorAll('.tab-button');
    
    // Add event listeners
    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    propertyValueSlider.addEventListener('input', function() {
        propertyValueDisplay.textContent = formatCurrency(this.value);
    });
    
    yearBuiltSlider.addEventListener('input', function() {
        yearBuiltDisplay.textContent = this.value;
    });
    
    applyFiltersButton.addEventListener('click', applyFilters);
    
    closeDetailsButton.addEventListener('click', function() {
        document.getElementById('property-details').classList.remove('active');
    });
    
    // Tab functionality
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons and tab contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding tab content
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    console.log('UI initialized');
}

// Format currency values
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
    }).format(value);
}

// Perform search
function performSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('searchResults');
    const query = searchInput.value.trim();
    
    if (query === '') {
        searchResults.innerHTML = '<div class="no-results">Enter a search term</div>';
        return;
    }
    
    // Show searching indicator
    searchResults.innerHTML = '<div class="no-results">Searching...</div>';
    
    // Try to search in wealthy individuals data first
    const foundInWealthyData = searchWealthyIndividuals(query);
    
    if (!foundInWealthyData) {
        // If not found in wealthy data, try to search by location
        markersGroup.clearLayers();
        
        // Use geocoding to search for the location
        geocodeLocation(query);
    }
}

// Apply filters
function applyFilters() {
    const propertyValueSlider = document.getElementById('property-value-slider');
    const yearBuiltSlider = document.getElementById('year-built-slider');
    const propertyTypes = Array.from(document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.value);
    
    console.log('Applying filters:');
    console.log('- Property Value:', formatCurrency(propertyValueSlider.value));
    console.log('- Year Built:', yearBuiltSlider.value);
    console.log('- Property Types:', propertyTypes);
    
    // In a real application, we would filter the data and update the map
    // For this demo, we'll just show an alert
    alert(`Filters applied:\n- Property Value: ${formatCurrency(propertyValueSlider.value)}\n- Year Built: ${yearBuiltSlider.value}\n- Property Types: ${propertyTypes.join(', ')}`);
}