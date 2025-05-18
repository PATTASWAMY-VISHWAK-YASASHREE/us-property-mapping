"""
Performance testing script using Locust.
Run with: locust -f tests/performance/locustfile.py
"""
import json
import random
import time
from locust import HttpUser, task, between, tag

class WealthMapUser(HttpUser):
    """
    Simulates a user of the Wealth Map platform.
    """
    # Wait between 1 and 5 seconds between tasks
    wait_time = between(1, 5)
    
    def on_start(self):
        """
        Initialize the user by logging in and storing the token.
        """
        # Login to get authentication token
        response = self.client.post(
            "/api/auth/login",
            data={
                "username": "user@example.com",
                "password": "userpassword"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
            self.user_id = None
            
            # Get user profile to store user ID
            user_response = self.client.get("/api/users/me", headers=self.headers)
            if user_response.status_code == 200:
                self.user_id = user_response.json()["id"]
        else:
            # If login fails, stop the user
            self.environment.runner.quit()
    
    @tag("auth")
    @task(1)
    def get_user_profile(self):
        """
        Get the current user's profile.
        """
        self.client.get("/api/users/me", headers=self.headers, name="/api/users/me")
    
    @tag("search")
    @task(5)
    def search_properties(self):
        """
        Search for properties with random criteria.
        """
        # Generate random search parameters
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        property_types = ["Single Family", "Condo", "Townhouse", "Multi-Family"]
        
        params = {
            "city": random.choice(cities),
            "property_type": random.choice(property_types),
            "min_price": random.randint(100000, 500000),
            "max_price": random.randint(500001, 2000000),
            "page": 1,
            "limit": 10
        }
        
        self.client.get(
            "/api/properties/search",
            params=params,
            headers=self.headers,
            name="/api/properties/search"
        )
    
    @tag("property")
    @task(3)
    def get_property_details(self):
        """
        Get details for a specific property.
        """
        # First, get a list of properties
        response = self.client.get(
            "/api/properties/",
            params={"limit": 20},
            headers=self.headers,
            name="/api/properties/"
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["items"]:
                # Select a random property
                property_id = random.choice(data["items"])["id"]
                
                # Get property details
                self.client.get(
                    f"/api/properties/{property_id}",
                    headers=self.headers,
                    name="/api/properties/{id}"
                )
    
    @tag("report")
    @task(2)
    def generate_report(self):
        """
        Generate a property report.
        """
        # First, get a list of properties
        response = self.client.get(
            "/api/properties/",
            params={"limit": 20},
            headers=self.headers,
            name="/api/properties/"
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["items"]:
                # Select a random property
                property_id = random.choice(data["items"])["id"]
                
                # Generate a report
                report_data = {
                    "property_id": property_id,
                    "report_type": random.choice(["basic", "standard", "premium"]),
                    "include_comparables": random.choice([True, False]),
                    "include_market_trends": random.choice([True, False])
                }
                
                self.client.post(
                    "/api/reports/",
                    json=report_data,
                    headers=self.headers,
                    name="/api/reports/"
                )
    
    @tag("dashboard")
    @task(1)
    def get_dashboard_stats(self):
        """
        Get dashboard statistics.
        """
        self.client.get(
            "/api/dashboard/stats",
            headers=self.headers,
            name="/api/dashboard/stats"
        )
    
    @tag("wealth")
    @task(2)
    def get_wealth_analysis(self):
        """
        Get wealth analysis for a property owner.
        """
        # First, get a list of properties
        response = self.client.get(
            "/api/properties/",
            params={"limit": 20},
            headers=self.headers,
            name="/api/properties/"
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["items"]:
                # Select a random property
                property = random.choice(data["items"])
                if property.get("owner_id"):
                    # Get wealth analysis for the owner
                    self.client.get(
                        f"/api/wealth/owner/{property['owner_id']}",
                        headers=self.headers,
                        name="/api/wealth/owner/{id}"
                    )
    
    @tag("admin")
    @task(1)
    def admin_tasks(self):
        """
        Perform admin tasks if the user is an admin.
        """
        # Check if user is admin
        if hasattr(self, "user_id"):
            user_response = self.client.get(f"/api/users/{self.user_id}", headers=self.headers)
            if user_response.status_code == 200 and user_response.json().get("role") == "admin":
                # Get list of users
                self.client.get(
                    "/api/admin/users",
                    params={"page": 1, "limit": 20},
                    headers=self.headers,
                    name="/api/admin/users"
                )
                
                # Get system stats
                self.client.get(
                    "/api/admin/stats",
                    headers=self.headers,
                    name="/api/admin/stats"
                )


class DatabaseBenchmarkUser(HttpUser):
    """
    User class specifically for benchmarking database performance.
    """
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Initialize the user by logging in as an admin.
        """
        # Login to get authentication token
        response = self.client.post(
            "/api/auth/login",
            data={
                "username": "admin@example.com",
                "password": "adminpassword"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            # If login fails, stop the user
            self.environment.runner.quit()
    
    @tag("db_benchmark")
    @task(1)
    def complex_property_query(self):
        """
        Perform a complex property query with multiple filters and joins.
        """
        # Generate random query parameters
        params = {
            "min_price": random.randint(100000, 500000),
            "max_price": random.randint(500001, 2000000),
            "min_bedrooms": random.randint(1, 3),
            "min_bathrooms": random.randint(1, 3),
            "property_types": random.sample(["Single Family", "Condo", "Townhouse", "Multi-Family"], 2),
            "cities": random.sample(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"], 2),
            "include_owner_details": True,
            "include_transaction_history": True,
            "sort_by": random.choice(["price", "date_listed", "square_feet"]),
            "sort_order": random.choice(["asc", "desc"]),
            "page": 1,
            "limit": 20
        }
        
        start_time = time.time()
        response = self.client.get(
            "/api/properties/advanced-search",
            params=params,
            headers=self.headers,
            name="/api/properties/advanced-search"
        )
        query_time = time.time() - start_time
        
        # Log the query time
        if response.status_code == 200:
            self.environment.events.request_success.fire(
                request_type="GET",
                name="DB Query Time",
                response_time=query_time * 1000,  # Convert to milliseconds
                response_length=len(response.content)
            )
    
    @tag("db_benchmark")
    @task(1)
    def aggregate_wealth_data(self):
        """
        Perform aggregation queries on wealth data.
        """
        # Generate random query parameters
        params = {
            "min_net_worth": random.randint(100000, 1000000),
            "group_by": random.choice(["city", "age_range", "income_bracket"]),
            "include_properties": random.choice([True, False]),
            "include_investments": random.choice([True, False])
        }
        
        start_time = time.time()
        response = self.client.get(
            "/api/wealth/aggregate",
            params=params,
            headers=self.headers,
            name="/api/wealth/aggregate"
        )
        query_time = time.time() - start_time
        
        # Log the query time
        if response.status_code == 200:
            self.environment.events.request_success.fire(
                request_type="GET",
                name="Wealth Aggregation Time",
                response_time=query_time * 1000,  # Convert to milliseconds
                response_length=len(response.content)
            )


class APIResponseTimeUser(HttpUser):
    """
    User class specifically for measuring API response times.
    """
    wait_time = between(0.1, 1)  # Shorter wait times for more intensive testing
    
    def on_start(self):
        """
        Initialize the user by logging in.
        """
        # Login to get authentication token
        response = self.client.post(
            "/api/auth/login",
            data={
                "username": "user@example.com",
                "password": "userpassword"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            # If login fails, stop the user
            self.environment.runner.quit()
    
    @tag("api_response")
    @task(10)
    def measure_search_response(self):
        """
        Measure response time for property search API.
        """
        # Generate random search parameters
        params = {
            "query": random.choice(["house", "apartment", "condo", "townhouse"]),
            "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
            "page": random.randint(1, 5),
            "limit": 10
        }
        
        self.client.get(
            "/api/properties/search",
            params=params,
            headers=self.headers,
            name="/api/properties/search (Response Time)"
        )
    
    @tag("api_response")
    @task(5)
    def measure_property_detail_response(self):
        """
        Measure response time for property detail API.
        """
        # First, get a list of properties
        response = self.client.get(
            "/api/properties/",
            params={"limit": 20},
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["items"]:
                # Select a random property
                property_id = random.choice(data["items"])["id"]
                
                # Measure response time for property details
                self.client.get(
                    f"/api/properties/{property_id}",
                    headers=self.headers,
                    name="/api/properties/{id} (Response Time)"
                )
    
    @tag("api_response")
    @task(3)
    def measure_report_generation_response(self):
        """
        Measure response time for report generation API.
        """
        # First, get a list of properties
        response = self.client.get(
            "/api/properties/",
            params={"limit": 20},
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["items"]:
                # Select a random property
                property_id = random.choice(data["items"])["id"]
                
                # Measure response time for report generation
                report_data = {
                    "property_id": property_id,
                    "report_type": "basic",
                    "include_comparables": False,
                    "include_market_trends": False
                }
                
                self.client.post(
                    "/api/reports/",
                    json=report_data,
                    headers=self.headers,
                    name="/api/reports/ (Response Time)"
                )