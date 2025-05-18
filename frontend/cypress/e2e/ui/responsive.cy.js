describe('Responsive Design Tests', () => {
  const pages = [
    { path: '/', name: 'Home' },
    { path: '/login', name: 'Login' },
    { path: '/dashboard', name: 'Dashboard' },
    { path: '/search', name: 'Search' },
    { path: '/reports', name: 'Reports' }
  ];
  
  const devices = [
    { name: 'Mobile', width: 375, height: 667 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Laptop', width: 1280, height: 800 },
    { name: 'Desktop', width: 1920, height: 1080 }
  ];
  
  // Mock authentication for protected routes
  beforeEach(() => {
    // Set up local storage with auth tokens to simulate logged-in state
    cy.window().then((win) => {
      win.localStorage.setItem('access_token', 'fake-access-token');
      win.localStorage.setItem('refresh_token', 'fake-refresh-token');
    });
    
    // Mock user profile API call
    cy.intercept('GET', '/api/users/me', {
      statusCode: 200,
      body: {
        id: '123',
        email: 'test@example.com',
        first_name: 'Test',
        last_name: 'User',
        role: 'admin'
      }
    }).as('userProfileRequest');
  });
  
  devices.forEach(device => {
    context(`${device.name} viewport (${device.width}x${device.height})`, () => {
      beforeEach(() => {
        // Set viewport for the current device
        cy.viewport(device.width, device.height);
      });
      
      pages.forEach(page => {
        it(`should display ${page.name} page correctly`, () => {
          cy.visit(page.path);
          
          // Wait for any API requests to complete
          if (page.path !== '/' && page.path !== '/login') {
            cy.wait('@userProfileRequest');
          }
          
          // Check that the page loaded without errors
          cy.get('body').should('be.visible');
          cy.get('main').should('be.visible');
          
          // No horizontal overflow should be present
          cy.window().then((win) => {
            const body = win.document.body;
            const html = win.document.documentElement;
            
            const hasHorizontalScroll = body.scrollWidth > win.innerWidth || html.scrollWidth > win.innerWidth;
            expect(hasHorizontalScroll).to.be.false;
          });
          
          // Navigation should be appropriate for the device size
          if (device.width < 768) {
            // Mobile: Check for hamburger menu
            cy.get('button[aria-label="Toggle navigation"]').should('be.visible');
            
            // Open mobile menu
            cy.get('button[aria-label="Toggle navigation"]').click();
            
            // Check that menu items are visible after clicking
            cy.get('nav').should('be.visible');
          } else {
            // Desktop/Tablet: Navigation should be visible by default
            cy.get('nav').should('be.visible');
            
            // No hamburger menu on larger screens
            cy.get('button[aria-label="Toggle navigation"]').should('not.exist');
          }
          
          // Take a screenshot for visual comparison
          cy.screenshot(`${page.name.toLowerCase()}-${device.name.toLowerCase()}`);
        });
      });
      
      // Test specific components that should adapt to different screen sizes
      it('should adapt search results layout', () => {
        // Mock search results
        cy.intercept('GET', '/api/search*', {
          statusCode: 200,
          body: {
            results: Array(5).fill().map((_, i) => ({
              id: `${i}`,
              address: `${i} Main St, Anytown, USA`,
              property_type: 'Single Family',
              bedrooms: 3,
              bathrooms: 2,
              square_feet: 1800,
              estimated_value: 450000
            })),
            total: 5
          }
        }).as('searchRequest');
        
        cy.visit('/search');
        cy.wait('@userProfileRequest');
        
        // Perform search
        cy.get('input[name="address"]').type('Main St');
        cy.get('button').contains('Search').click();
        cy.wait('@searchRequest');
        
        // Check search results layout
        cy.get('[data-testid="search-results"]').should('be.visible');
        
        if (device.width < 768) {
          // On mobile, results should stack vertically
          cy.get('[data-testid="search-result-item"]').should('have.css', 'flex-direction', 'column');
        } else {
          // On larger screens, results might have a different layout
          cy.get('[data-testid="search-result-item"]').should('be.visible');
        }
      });
      
      it('should adapt dashboard layout', () => {
        // Mock dashboard data
        cy.intercept('GET', '/api/dashboard/stats', {
          statusCode: 200,
          body: {
            total_properties: 150,
            total_reports: 75,
            recent_searches: 25,
            premium_reports: 30
          }
        }).as('dashboardStatsRequest');
        
        cy.visit('/dashboard');
        cy.wait('@userProfileRequest');
        cy.wait('@dashboardStatsRequest');
        
        // Check dashboard layout
        cy.get('[data-testid="dashboard-stats"]').should('be.visible');
        
        if (device.width < 768) {
          // On mobile, stats cards should stack vertically
          cy.get('[data-testid="stats-grid"]').should('have.css', 'grid-template-columns', '1fr');
        } else if (device.width < 1280) {
          // On tablet, stats might be in a 2x2 grid
          cy.get('[data-testid="stats-grid"]').should('have.css', 'grid-template-columns', '1fr 1fr');
        } else {
          // On desktop, stats might be in a row
          cy.get('[data-testid="stats-grid"]').should('have.css', 'grid-template-columns', '1fr 1fr 1fr 1fr');
        }
      });
    });
  });
});