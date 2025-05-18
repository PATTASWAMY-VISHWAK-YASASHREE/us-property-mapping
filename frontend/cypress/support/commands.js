// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

// -- Custom Login Command --
Cypress.Commands.add('login', (email = 'test@example.com', password = 'password123') => {
  cy.visit('/login');
  
  // Intercept the login request
  cy.intercept('POST', '/api/auth/login', {
    statusCode: 200,
    body: {
      access_token: 'fake-access-token',
      refresh_token: 'fake-refresh-token',
      token_type: 'bearer',
      expires_in: 3600
    }
  }).as('loginRequest');
  
  // Fill in login form
  cy.get('input[type="email"]').type(email);
  cy.get('input[type="password"]').type(password);
  cy.get('button[type="submit"]').click();
  
  // Wait for login request to complete
  cy.wait('@loginRequest');
  
  // Verify we're redirected to dashboard
  cy.url().should('include', '/dashboard');
});

// -- Custom Logout Command --
Cypress.Commands.add('logout', () => {
  // Click on user menu
  cy.get('[data-testid="user-menu"]').click();
  
  // Click logout button
  cy.contains('Logout').click();
  
  // Verify we're redirected to login page
  cy.url().should('include', '/login');
});

// -- Custom Search Property Command --
Cypress.Commands.add('searchProperty', (address) => {
  // Navigate to search page
  cy.visit('/search');
  
  // Mock search results
  cy.intercept('GET', '/api/search*', {
    statusCode: 200,
    body: {
      results: [
        {
          id: '123',
          address: '123 Main St, Anytown, USA',
          property_type: 'Single Family',
          bedrooms: 3,
          bathrooms: 2,
          square_feet: 1800,
          estimated_value: 450000
        }
      ],
      total: 1
    }
  }).as('searchRequest');
  
  // Perform search
  cy.get('input[name="address"]').type(address);
  cy.get('button').contains('Search').click();
  
  // Wait for search results
  cy.wait('@searchRequest');
});

// -- Custom Generate Report Command --
Cypress.Commands.add('generateReport', (propertyId = '123', reportType = 'standard') => {
  // Navigate to property page
  cy.visit(`/property/${propertyId}`);
  
  // Mock property details
  cy.intercept('GET', `/api/properties/${propertyId}`, {
    statusCode: 200,
    body: {
      id: propertyId,
      address: '123 Main St, Anytown, USA',
      property_type: 'Single Family',
      bedrooms: 3,
      bathrooms: 2,
      square_feet: 1800,
      estimated_value: 450000
    }
  }).as('propertyRequest');
  
  cy.wait('@propertyRequest');
  
  // Click generate report button
  cy.contains('Generate Report').click();
  
  // Mock report options
  cy.intercept('GET', '/api/reports/options', {
    statusCode: 200,
    body: {
      report_types: [
        { id: 'basic', name: 'Basic Report', price: 0 },
        { id: 'standard', name: 'Standard Report', price: 9.99 },
        { id: 'premium', name: 'Premium Report', price: 19.99 }
      ]
    }
  }).as('reportOptionsRequest');
  
  cy.wait('@reportOptionsRequest');
  
  // Select report type
  cy.get(`input[value="${reportType}"]`).check();
  
  // Mock report generation
  cy.intercept('POST', '/api/reports', {
    statusCode: 200,
    body: {
      id: '789',
      property_id: propertyId,
      report_type: reportType,
      created_at: new Date().toISOString(),
      status: 'completed',
      download_url: 'https://example.com/reports/789.pdf'
    }
  }).as('createReportRequest');
  
  // Submit report generation form
  cy.contains('Generate').click();
  cy.wait('@createReportRequest');
});

// -- Custom Check Accessibility Command --
Cypress.Commands.add('checkA11y', (context, options) => {
  cy.injectAxe();
  cy.checkA11y(context, options);
});