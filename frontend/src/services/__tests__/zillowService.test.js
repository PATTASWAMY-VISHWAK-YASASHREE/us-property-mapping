import { describe, it, expect, vi, beforeEach } from 'vitest';
import zillowService from '../zillowService';

// Mock XMLHttpRequest
global.XMLHttpRequest = class {
  constructor() {
    this.withCredentials = false;
    this.readyState = 4; // DONE
    this.status = 200;
    this.responseText = JSON.stringify({ success: true, data: [] });
    this.headers = {};
  }

  open(method, url) {
    this.method = method;
    this.url = url;
  }

  setRequestHeader(name, value) {
    this.headers[name] = value;
  }

  send() {
    // Simulate async response
    setTimeout(() => {
      if (this.onreadystatechange) {
        this.onreadystatechange();
      }
    }, 0);
  }

  addEventListener(event, callback) {
    if (event === 'readystatechange') {
      this.onreadystatechange = callback;
    }
  }
};

describe('zillowService', () => {
  beforeEach(() => {
    vi.spyOn(global, 'XMLHttpRequest');
  });

  it('should use the correct API key for searchByAddress', async () => {
    const promise = zillowService.searchByAddress('123 Main St');
    
    // Wait for the promise to resolve
    await promise;
    
    // Check that XMLHttpRequest was called
    expect(XMLHttpRequest).toHaveBeenCalled();
    
    // Get the instance
    const xhr = XMLHttpRequest.mock.instances[0];
    
    // Check that the correct headers were set
    expect(xhr.headers['x-rapidapi-key']).toBe('39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75');
    expect(xhr.headers['x-rapidapi-host']).toBe('zillow-working-api.p.rapidapi.com');
    
    // Check that the correct URL was used
    expect(xhr.url).toContain('https://zillow-working-api.p.rapidapi.com/autocomplete');
    expect(xhr.url).toContain('query=123%20Main%20St');
  });

  it('should use the correct API key for searchByLocation', async () => {
    const promise = zillowService.searchByLocation('New York, NY');
    
    // Wait for the promise to resolve
    await promise;
    
    // Check that XMLHttpRequest was called
    expect(XMLHttpRequest).toHaveBeenCalled();
    
    // Get the instance
    const xhr = XMLHttpRequest.mock.instances[0];
    
    // Check that the correct headers were set
    expect(xhr.headers['x-rapidapi-key']).toBe('39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75');
    expect(xhr.headers['x-rapidapi-host']).toBe('zillow-working-api.p.rapidapi.com');
    
    // Check that the correct URL was used
    expect(xhr.url).toContain('https://zillow-working-api.p.rapidapi.com/search/byaddress');
    expect(xhr.url).toContain('location=New%20York%2C%20NY');
  });

  it('should use the correct API key for searchPropertiesByCoordinates', async () => {
    const promise = zillowService.searchPropertiesByCoordinates(37.7749, -122.4194);
    
    // Wait for the promise to resolve
    await promise;
    
    // Check that XMLHttpRequest was called
    expect(XMLHttpRequest).toHaveBeenCalled();
    
    // Get the instance
    const xhr = XMLHttpRequest.mock.instances[0];
    
    // Check that the correct headers were set
    expect(xhr.headers['x-rapidapi-key']).toBe('39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75');
    expect(xhr.headers['x-rapidapi-host']).toBe('zillow-working-api.p.rapidapi.com');
    
    // Check that the correct URL was used
    expect(xhr.url).toContain('https://zillow-working-api.p.rapidapi.com/search/bycoordinates');
    expect(xhr.url).toContain('latitude=37.7749');
    expect(xhr.url).toContain('longitude=-122.4194');
  });
});