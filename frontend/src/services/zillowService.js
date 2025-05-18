/**
 * Zillow API Service
 * 
 * This service provides methods to interact with the Zillow API through RapidAPI
 * using the code snippets provided in code_snippets.txt
 */

// Zillow RapidAPI key
const ZILLOW_API_KEY = '39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75';
const ZILLOW_API_HOST = 'zillow-working-api.p.rapidapi.com';

/**
 * Search for properties by address
 * @param {string} query - The address to search for
 * @returns {Promise} - Promise that resolves with the search results
 */
export function searchByAddress(query) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          const response = JSON.parse(this.responseText);
          resolve(response);
        } catch (error) {
          reject(error);
        }
      }
    });

    // Encode the query for URL
    const encodedQuery = encodeURIComponent(query);
    xhr.open('GET', `https://zillow-working-api.p.rapidapi.com/autocomplete?query=${encodedQuery}`);
    xhr.setRequestHeader('x-rapidapi-key', ZILLOW_API_KEY);
    xhr.setRequestHeader('x-rapidapi-host', ZILLOW_API_HOST);

    xhr.send(null);
  });
}

/**
 * Search for properties by location
 * @param {string} location - The location to search for (e.g., "New York, NY")
 * @param {number} page - Page number for results
 * @returns {Promise} - Promise that resolves with the search results
 */
export function searchByLocation(location, page = 1) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          const response = JSON.parse(this.responseText);
          resolve(response);
        } catch (error) {
          reject(error);
        }
      }
    });

    // Encode the location for URL
    const encodedLocation = encodeURIComponent(location);
    xhr.open('GET', `https://zillow-working-api.p.rapidapi.com/search/byaddress?location=${encodedLocation}&page=${page}&sortOrder=Homes_for_you&listingStatus=For_Sale&bed_min=No_Min&bed_max=No_Max&bathrooms=Any&homeType=Houses%2C%20Townhomes%2C%20Multi-family%2C%20Condos%2FCo-ops%2C%20Lots-Land%2C%20Apartments%2C%20Manufactured&maxHOA=Any&listingType=By_Agent&listingTypeOptions=Agent%20listed%2CNew%20Construction%2CFore-closures%2CAuctions&parkingSpots=Any&mustHaveBasement=No&daysOnZillow=Any&soldInLast=Any`);
    xhr.setRequestHeader('x-rapidapi-key', ZILLOW_API_KEY);
    xhr.setRequestHeader('x-rapidapi-host', ZILLOW_API_HOST);

    xhr.send(null);
  });
}

/**
 * Get property details by address
 * @param {string} propertyAddress - The full property address
 * @returns {Promise} - Promise that resolves with the property details
 */
export function getPropertyDetailsByAddress(propertyAddress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          const response = JSON.parse(this.responseText);
          resolve(response);
        } catch (error) {
          reject(error);
        }
      }
    });

    // Encode the address for URL
    const encodedAddress = encodeURIComponent(propertyAddress);
    xhr.open('GET', `https://zillow-working-api.p.rapidapi.com/pro/byaddress?propertyaddress=${encodedAddress}`);
    xhr.setRequestHeader('x-rapidapi-key', ZILLOW_API_KEY);
    xhr.setRequestHeader('x-rapidapi-host', ZILLOW_API_HOST);

    xhr.send(null);
  });
}

/**
 * Get similar properties
 * @param {Object} params - Parameters for similar properties search
 * @param {string} params.zpid - Zillow property ID
 * @param {string} params.url - Zillow property URL
 * @param {string} params.address - Property address
 * @returns {Promise} - Promise that resolves with similar properties
 */
export function getSimilarProperties(params) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          const response = JSON.parse(this.responseText);
          resolve(response);
        } catch (error) {
          reject(error);
        }
      }
    });

    // Build the URL with parameters
    let url = 'https://zillow-working-api.p.rapidapi.com/similar?';
    if (params.zpid) url += `byzpid=${params.zpid}&`;
    if (params.url) url += `byurl=${encodeURIComponent(params.url)}&`;
    if (params.address) url += `byaddress=${encodeURIComponent(params.address)}&`;
    if (params.lotid) url += `bylotid=${params.lotid}`;

    xhr.open('GET', url);
    xhr.setRequestHeader('x-rapidapi-key', ZILLOW_API_KEY);
    xhr.setRequestHeader('x-rapidapi-host', ZILLOW_API_HOST);

    xhr.send(null);
  });
}

/**
 * Get nearby properties
 * @param {Object} params - Parameters for nearby properties search
 * @param {string} params.zpid - Zillow property ID
 * @param {string} params.url - Zillow property URL
 * @param {string} params.address - Property address
 * @returns {Promise} - Promise that resolves with nearby properties
 */
export function getNearbyProperties(params) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          const response = JSON.parse(this.responseText);
          resolve(response);
        } catch (error) {
          reject(error);
        }
      }
    });

    // Build the URL with parameters
    let url = 'https://zillow-working-api.p.rapidapi.com/nearby?';
    if (params.zpid) url += `byzpid=${params.zpid}&`;
    if (params.url) url += `byurl=${encodeURIComponent(params.url)}&`;
    if (params.address) url += `byaddress=${encodeURIComponent(params.address)}&`;
    if (params.lotid) url += `bylotid=${params.lotid}`;

    xhr.open('GET', url);
    xhr.setRequestHeader('x-rapidapi-key', ZILLOW_API_KEY);
    xhr.setRequestHeader('x-rapidapi-host', ZILLOW_API_HOST);

    xhr.send(null);
  });
}

/**
 * Get price history for a property
 * @param {Object} params - Parameters for price history search
 * @param {string} params.zpid - Zillow property ID
 * @param {string} params.url - Zillow property URL
 * @param {string} params.address - Property address
 * @returns {Promise} - Promise that resolves with price history
 */
export function getPriceHistory(params) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          const response = JSON.parse(this.responseText);
          resolve(response);
        } catch (error) {
          reject(error);
        }
      }
    });

    // Build the URL with parameters
    let url = 'https://zillow-working-api.p.rapidapi.com/pricehistory?';
    if (params.zpid) url += `byzpid=${params.zpid}&`;
    if (params.url) url += `byurl=${encodeURIComponent(params.url)}&`;
    if (params.address) url += `byaddress=${encodeURIComponent(params.address)}`;

    xhr.open('GET', url);
    xhr.setRequestHeader('x-rapidapi-key', ZILLOW_API_KEY);
    xhr.setRequestHeader('x-rapidapi-host', ZILLOW_API_HOST);

    xhr.send(null);
  });
}

/**
 * Get apartment details
 * @param {Object} params - Parameters for apartment details search
 * @param {string} params.lotid - Lot ID
 * @param {string} params.apturl - Apartment URL
 * @returns {Promise} - Promise that resolves with apartment details
 */
export function getApartmentDetails(params) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          const response = JSON.parse(this.responseText);
          resolve(response);
        } catch (error) {
          reject(error);
        }
      }
    });

    // Build the URL with parameters
    let url = 'https://zillow-working-api.p.rapidapi.com/apartment_details?';
    if (params.lotid) url += `bylotid=${params.lotid}&`;
    if (params.apturl) url += `byapturl=${encodeURIComponent(params.apturl)}`;

    xhr.open('GET', url);
    xhr.setRequestHeader('x-rapidapi-key', ZILLOW_API_KEY);
    xhr.setRequestHeader('x-rapidapi-host', ZILLOW_API_HOST);

    xhr.send(null);
  });
}

/**
 * Search properties by coordinates
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @param {number} radius - Search radius in miles
 * @returns {Promise} - Promise that resolves with properties in the area
 */
export function searchPropertiesByCoordinates(lat, lng, radius = 0.5) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener('readystatechange', function () {
      if (this.readyState === this.DONE) {
        try {
          const response = JSON.parse(this.responseText);
          resolve(response);
        } catch (error) {
          reject(error);
        }
      }
    });

    xhr.open('GET', `https://zillow-working-api.p.rapidapi.com/search/bycoordinates?latitude=${lat}&longitude=${lng}&radius=${radius}&page=1&sortOrder=Homes_for_you&listingStatus=For_Sale&bed_min=No_Min&bed_max=No_Max&bathrooms=Any&homeType=Houses%2C%20Townhomes%2C%20Multi-family%2C%20Condos%2FCo-ops%2C%20Lots-Land%2C%20Apartments%2C%20Manufactured&maxHOA=Any&listingType=By_Agent&listingTypeOptions=Agent%20listed%2CNew%20Construction%2CFore-closures%2CAuctions&parkingSpots=Any&daysOnZillow=Any&soldInLast=Any`);
    xhr.setRequestHeader('x-rapidapi-key', ZILLOW_API_KEY);
    xhr.setRequestHeader('x-rapidapi-host', ZILLOW_API_HOST);

    xhr.send(null);
  });
}

export default {
  searchByAddress,
  searchByLocation,
  getPropertyDetailsByAddress,
  getSimilarProperties,
  getNearbyProperties,
  getPriceHistory,
  getApartmentDetails,
  searchPropertiesByCoordinates
};