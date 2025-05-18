from app.services.zillow_api import ZillowAPIService

def test_zillow_api():
    # Create an instance of the ZillowAPIService
    zillow_service = ZillowAPIService()
    
    # Check that the API key is set correctly
    assert zillow_service.api_key == "39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75"
    assert zillow_service.headers["X-RapidAPI-Key"] == "39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75"
    assert zillow_service.headers["X-RapidAPI-Host"] == "zillow-working-api.p.rapidapi.com"
    
    # Check that the base URL is set correctly
    assert zillow_service.BASE_URL == "https://zillow-working-api.p.rapidapi.com"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_zillow_api()