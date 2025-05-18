describe('Report Generation Flow', () => {
  beforeEach(() => {
    // Login before each test
    cy.visit('/login');
    
    // Mock successful login
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: {
        access_token: 'fake-access-token',
        refresh_token: 'fake-refresh-token',
        token_type: 'bearer',
        expires_in: 3600
      }
    }).as('loginRequest');
    
    cy.get('input[type="email"]').type('test@example.com');
    cy.get('input[type="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    cy.wait('@loginRequest');
    
    // Ensure we're on the dashboard
    cy.url().should('include', '/dashboard');
  });

  it('should generate a property report', () => {
    // Mock property search results
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
            year_built: 2005,
            lot_size: 0.25,
            estimated_value: 450000
          }
        ],
        total: 1
      }
    }).as('searchRequest');
    
    // Navigate to search page
    cy.get('nav').contains('Search').click();
    cy.url().should('include', '/search');
    
    // Perform a search
    cy.get('input[name="address"]').type('123 Main St');
    cy.get('button').contains('Search').click();
    cy.wait('@searchRequest');
    
    // Select the property from search results
    cy.contains('123 Main St, Anytown, USA').click();
    
    // Mock property details
    cy.intercept('GET', '/api/properties/*', {
      statusCode: 200,
      body: {
        id: '123',
        address: '123 Main St, Anytown, USA',
        property_type: 'Single Family',
        bedrooms: 3,
        bathrooms: 2,
        square_feet: 1800,
        year_built: 2005,
        lot_size: 0.25,
        estimated_value: 450000,
        owner: {
          id: '456',
          name: 'John Doe',
          email: 'john@example.com'
        },
        images: [
          { id: '1', url: 'https://example.com/image1.jpg' }
        ]
      }
    }).as('propertyRequest');
    
    // Wait for property details to load
    cy.wait('@propertyRequest');
    cy.url().should('include', '/property/123');
    
    // Click on generate report button
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
    cy.get('input[value="standard"]').check();
    
    // Mock report generation
    cy.intercept('POST', '/api/reports', {
      statusCode: 200,
      body: {
        id: '789',
        property_id: '123',
        report_type: 'standard',
        created_at: new Date().toISOString(),
        status: 'processing',
        download_url: null
      }
    }).as('createReportRequest');
    
    // Submit report generation form
    cy.contains('Generate').click();
    cy.wait('@createReportRequest');
    
    // Mock report status check
    cy.intercept('GET', '/api/reports/789', {
      statusCode: 200,
      body: {
        id: '789',
        property_id: '123',
        report_type: 'standard',
        created_at: new Date().toISOString(),
        status: 'completed',
        download_url: 'https://example.com/reports/789.pdf'
      }
    }).as('reportStatusRequest');
    
    // Wait for report to be ready (in a real test, we might need to poll)
    cy.contains('Processing').should('be.visible');
    
    // Force a check of the report status
    cy.wait(1000); // Simulate waiting for report generation
    cy.get('button').contains('Check Status').click();
    cy.wait('@reportStatusRequest');
    
    // Verify download link appears
    cy.contains('Download Report').should('be.visible')
      .and('have.attr', 'href', 'https://example.com/reports/789.pdf');
  });

  it('should handle report generation errors', () => {
    // Navigate to reports page
    cy.get('nav').contains('Reports').click();
    cy.url().should('include', '/reports');
    
    // Mock existing reports
    cy.intercept('GET', '/api/reports', {
      statusCode: 200,
      body: {
        reports: [
          {
            id: '789',
            property_id: '123',
            property_address: '123 Main St, Anytown, USA',
            report_type: 'standard',
            created_at: new Date().toISOString(),
            status: 'completed',
            download_url: 'https://example.com/reports/789.pdf'
          }
        ]
      }
    }).as('reportsRequest');
    
    cy.wait('@reportsRequest');
    
    // Try to regenerate a report
    cy.contains('Regenerate').click();
    
    // Mock error response
    cy.intercept('POST', '/api/reports', {
      statusCode: 400,
      body: {
        detail: 'Report generation failed: insufficient data'
      }
    }).as('failedReportRequest');
    
    // Submit report generation form
    cy.contains('Generate').click();
    cy.wait('@failedReportRequest');
    
    // Verify error message
    cy.contains('Report generation failed').should('be.visible');
  });
});