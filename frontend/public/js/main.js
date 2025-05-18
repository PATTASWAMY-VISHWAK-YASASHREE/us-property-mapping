// Main entry point for the Wealth Map Platform

// Wait for the document to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map
    initMap();
    
    // Initialize UI elements
    initUI();
    
    // Load wealthy individuals data
    loadWealthyIndividualsData()
        .then(() => {
            console.log('Application initialized successfully');
        })
        .catch(error => {
            console.error('Error initializing application:', error);
        });
    
    // Add custom search functionality
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const searchResults = document.createElement('div');
    searchResults.id = 'searchResults';
    document.querySelector('.search-container').appendChild(searchResults);
    
    // Override the search button click handler
    if (searchButton) {
        const originalClickHandler = searchButton.onclick;
        searchButton.onclick = function() {
            if (typeof customSearch === 'function') {
                customSearch();
            } else if (typeof performSearch === 'function') {
                performSearch();
            } else if (originalClickHandler) {
                originalClickHandler();
            }
        };
    }
    
    // Override the search input keyup handler
    if (searchInput) {
        const originalKeyupHandler = searchInput.onkeyup;
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                if (typeof customSearch === 'function') {
                    customSearch();
                } else if (typeof performSearch === 'function') {
                    performSearch();
                } else if (originalKeyupHandler) {
                    originalKeyupHandler(e);
                }
            }
        });
    }
});