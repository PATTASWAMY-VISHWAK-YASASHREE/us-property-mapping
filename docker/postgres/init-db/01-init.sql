-- Initialize the wealth_map database
-- This script runs when the PostgreSQL container starts

-- Create the database if it doesn't exist
-- Note: This is redundant as the POSTGRES_DB environment variable already creates the database
-- But we include it for clarity
SELECT 'CREATE DATABASE wealth_map' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'wealth_map');

-- Connect to the wealth_map database
\c wealth_map;

-- Create a message table to verify the database is working
CREATE TABLE IF NOT EXISTS db_info (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert a verification message
INSERT INTO db_info (message) VALUES ('EDB PostgreSQL server up and running. Database name: wealth_map, Password: vishwak');

-- Grant privileges
ALTER USER postgres WITH PASSWORD 'vishwak';