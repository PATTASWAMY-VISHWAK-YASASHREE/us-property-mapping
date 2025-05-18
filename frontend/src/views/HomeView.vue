<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>Wealth Map Platform</h1>
        <p class="tagline">Discover, analyze, and visualize property wealth data</p>
        <div class="hero-actions">
          <router-link to="/register" class="btn-primary">Get Started</router-link>
          <router-link to="/login" class="btn-secondary">Login</router-link>
        </div>
      </div>
    </section>
    
    <section class="features">
      <h2>Platform Features</h2>
      <div class="feature-cards">
        <div class="feature-card">
          <div class="feature-icon">🏠</div>
          <h3>Property Analysis</h3>
          <p>Comprehensive data on millions of properties across the country</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">🗺️</div>
          <h3>Interactive Maps</h3>
          <p>Visualize property data with our advanced mapping tools</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">💰</div>
          <h3>Wealth Insights</h3>
          <p>Understand wealth distribution and ownership patterns</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Custom Reports</h3>
          <p>Generate detailed reports tailored to your specific needs</p>
        </div>
      </div>
    </section>
    
    <section class="how-it-works">
      <h2>How It Works</h2>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Create an Account</h3>
          <p>Sign up for access to our comprehensive property database</p>
        </div>
        
        <div class="step">
          <div class="step-number">2</div>
          <h3>Search Properties</h3>
          <p>Find properties by address, owner, value, or location</p>
        </div>
        
        <div class="step">
          <div class="step-number">3</div>
          <h3>Analyze Data</h3>
          <p>Explore detailed information about properties and owners</p>
        </div>
        
        <div class="step">
          <div class="step-number">4</div>
          <h3>Generate Reports</h3>
          <p>Create custom reports and export data for your needs</p>
        </div>
      </div>
    </section>
    
    <section class="cta">
      <div class="cta-content">
        <h2>Ready to get started?</h2>
        <p>Join thousands of professionals using our platform for property research and wealth analysis</p>
        <router-link to="/register" class="btn-primary">Create Your Account</router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
// No additional script needed for this view
</script>

<style scoped>
.home {
  color: #333;
}

.hero {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.tagline {
  font-size: 24px;
  margin-bottom: 40px;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn-primary {
  background-color: white;
  color: #4CAF50;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 18px;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #f0f0f0;
}

.btn-secondary {
  background-color: transparent;
  color: white;
  border: 2px solid white;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 18px;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.3s;
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.features, .how-it-works {
  padding: 80px 20px;
  text-align: center;
}

h2 {
  font-size: 36px;
  margin-bottom: 40px;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 24px;
  margin-bottom: 15px;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.step {
  position: relative;
  padding: 30px;
}

.step-number {
  background-color: #4CAF50;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin: 0 auto 20px;
}

.step h3 {
  font-size: 24px;
  margin-bottom: 15px;
}

.cta {
  background-color: #f5f5f5;
  padding: 80px 20px;
  text-align: center;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta h2 {
  font-size: 36px;
  margin-bottom: 20px;
}

.cta p {
  font-size: 18px;
  margin-bottom: 30px;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 36px;
  }
  
  .tagline {
    font-size: 20px;
  }
  
  .hero-actions {
    flex-direction: column;
    gap: 15px;
  }
  
  h2 {
    font-size: 30px;
  }
}
</style>