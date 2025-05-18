describe('Login Flow', () => {
  beforeEach(() => {
    // Visit the login page before each test
    cy.visit('/login');
  });

  it('should display login form', () => {
    cy.get('form').should('be.visible');
    cy.get('input[type="email"]').should('be.visible');
    cy.get('input[type="password"]').should('be.visible');
    cy.get('button[type="submit"]').should('be.visible');
  });

  it('should show validation errors for empty fields', () => {
    cy.get('button[type="submit"]').click();
    cy.get('form').contains('Email is required').should('be.visible');
    cy.get('form').contains('Password is required').should('be.visible');
  });

  it('should show error for invalid credentials', () => {
    cy.get('input[type="email"]').type('invalid@example.com');
    cy.get('input[type="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();
    
    // Intercept the API call and mock a 401 response
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 401,
      body: { detail: 'Invalid credentials' }
    }).as('loginRequest');
    
    cy.wait('@loginRequest');
    cy.contains('Invalid credentials').should('be.visible');
  });

  it('should redirect to dashboard after successful login', () => {
    cy.get('input[type="email"]').type('test@example.com');
    cy.get('input[type="password"]').type('password123');
    
    // Intercept the API call and mock a successful response
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: {
        access_token: 'fake-access-token',
        refresh_token: 'fake-refresh-token',
        token_type: 'bearer',
        expires_in: 3600
      }
    }).as('loginRequest');
    
    cy.get('button[type="submit"]').click();
    cy.wait('@loginRequest');
    
    // Check that we're redirected to the dashboard
    cy.url().should('include', '/dashboard');
  });

  it('should handle MFA flow when required', () => {
    cy.get('input[type="email"]').type('mfa@example.com');
    cy.get('input[type="password"]').type('password123');
    
    // Intercept the API call and mock a response requiring MFA
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: {
        access_token: 'fake-access-token',
        token_type: 'bearer',
        mfa_required: true
      }
    }).as('loginRequest');
    
    cy.get('button[type="submit"]').click();
    cy.wait('@loginRequest');
    
    // Check that MFA input is displayed
    cy.get('input[type="text"][name="mfa_code"]').should('be.visible');
    
    // Enter MFA code
    cy.get('input[type="text"][name="mfa_code"]').type('123456');
    
    // Intercept the MFA verification API call
    cy.intercept('POST', '/api/auth/verify-mfa', {
      statusCode: 200,
      body: {
        access_token: 'fake-full-access-token',
        refresh_token: 'fake-refresh-token',
        token_type: 'bearer',
        expires_in: 3600
      }
    }).as('mfaRequest');
    
    cy.get('button').contains('Verify').click();
    cy.wait('@mfaRequest');
    
    // Check that we're redirected to the dashboard
    cy.url().should('include', '/dashboard');
  });
});