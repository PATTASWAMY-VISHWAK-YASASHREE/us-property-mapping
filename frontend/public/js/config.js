// Configuration settings for the Wealth Map Platform

export const CONFIG = {
    // Map configuration
    map: {
        center: [39.8283, -98.5795], // Center of the US
        zoom: 4,
        minZoom: 3,
        maxZoom: 18,
        tileLayer: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    },
    
    // API endpoints
    api: {
        properties: '/api/properties',
        owners: '/api/owners',
        search: '/api/search',
        wealth: '/api/wealth',
        reports: '/api/reports'
    },
    
    // Data sources
    dataSources: {
        wealthyIndividuals: '/data/wealthy-properties.json',
        countyRecords: '/api/data/county-records',
        taxAssessor: '/api/data/tax-assessor',
        census: '/api/data/census',
        businessRegistrations: '/api/data/business-registrations'
    },
    
    // Search settings
    search: {
        minQueryLength: 3,
        maxResults: 50,
        searchDelay: 300 // ms
    },
    
    // UI settings
    ui: {
        propertyColors: {
            residential: '#4CAF50',
            commercial: '#2196F3',
            industrial: '#FF9800',
            land: '#9C27B0'
        },
        wealthRangeColors: [
            '#FFEB3B', // < $1M
            '#FFC107', // $1M - $10M
            '#FF9800', // $10M - $50M
            '#FF5722', // $50M - $100M
            '#E91E63', // $100M - $500M
            '#9C27B0'  // > $500M
        ]
    }
};