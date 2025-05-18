from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import time

from app.core.config import settings

# Configure engine with optimized pool settings for high concurrency
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,  # Increase connection pool size for 500+ concurrent users
    max_overflow=30,  # Allow additional connections when pool is full
    pool_timeout=30,  # Timeout for getting connection from pool
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Check connection validity before using from pool
    poolclass=QueuePool  # Use QueuePool for better performance
)

# Optimize query execution
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()
    
@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_time = time.time() - context._query_start_time
    if total_time > 0.1:  # Log slow queries (over 100ms)
        import logging
        logging.warning(f"Slow query detected ({total_time:.2f}s): {statement}")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()