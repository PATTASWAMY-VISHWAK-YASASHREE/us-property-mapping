FROM postgres:15

# Install PostGIS extension
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-15-postgis-3 \
        postgresql-15-postgis-3-scripts \
    && rm -rf /var/lib/apt/lists/*

# Initialize PostGIS extension
COPY ./init-postgis.sql /docker-entrypoint-initdb.d/