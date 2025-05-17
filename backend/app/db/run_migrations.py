import os
import logging
from pathlib import Path

from sqlalchemy import text
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run SQL migrations from the migrations directory."""
    migrations_dir = Path(__file__).parent / "migrations"
    
    if not migrations_dir.exists():
        logger.error(f"Migrations directory not found: {migrations_dir}")
        return
    
    # Get all SQL files in the migrations directory
    migration_files = sorted([f for f in migrations_dir.glob("*.sql")])
    
    if not migration_files:
        logger.warning("No migration files found.")
        return
    
    # Execute each migration file
    for migration_file in migration_files:
        logger.info(f"Running migration: {migration_file.name}")
        
        # Read the SQL file
        with open(migration_file, "r") as f:
            sql = f.read()
        
        # Execute the SQL
        with engine.begin() as conn:
            conn.execute(text(sql))
        
        logger.info(f"Migration completed: {migration_file.name}")

if __name__ == "__main__":
    logger.info("Running database migrations...")
    run_migrations()
    logger.info("Database migrations completed.")