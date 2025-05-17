# Wealth Map Platform Project Structure

```
/wealth-map/
├── frontend/                      # Vue.js 3 frontend
│   ├── public/                    # Static assets
│   ├── src/                       # Source code
│   │   ├── assets/                # Images, fonts, etc.
│   │   ├── components/            # Vue components
│   │   │   ├── auth/              # Authentication components
│   │   │   ├── map/               # Map-related components
│   │   │   ├── property/          # Property components
│   │   │   ├── search/            # Search components
│   │   │   └── wealth/            # Wealth analysis components
│   │   ├── composables/           # Vue 3 composables
│   │   ├── router/                # Vue Router configuration
│   │   ├── stores/                # Pinia stores
│   │   ├── views/                 # Page components
│   │   ├── App.vue                # Root component
│   │   └── main.js                # Entry point
│   ├── .env                       # Environment variables
│   ├── package.json               # Dependencies
│   └── vite.config.js             # Vite configuration
├── backend/                       # FastAPI backend
│   ├── app/                       # Application code
│   │   ├── api/                   # API endpoints
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── properties.py      # Property endpoints
│   │   │   ├── users.py           # User endpoints
│   │   │   ├── companies.py       # Company endpoints
│   │   │   ├── wealth.py          # Wealth data endpoints
│   │   │   └── reports.py         # Report endpoints
│   │   ├── core/                  # Core functionality
│   │   │   ├── config.py          # Configuration
│   │   │   ├── security.py        # Security utilities
│   │   │   └── dependencies.py    # FastAPI dependencies
│   │   ├── db/                    # Database
│   │   │   ├── base.py            # Base models
│   │   │   ├── session.py         # Database session
│   │   │   └── init_db.py         # Database initialization
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/              # Business logic
│   │   │   ├── auth.py            # Authentication service
│   │   │   ├── property.py        # Property service
│   │   │   ├── user.py            # User service
│   │   │   ├── company.py         # Company service
│   │   │   ├── wealth.py          # Wealth data service
│   │   │   └── report.py          # Report service
│   │   └── main.py                # FastAPI application
│   ├── alembic/                   # Database migrations
│   ├── tests/                     # Tests
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Environment variables
├── docker/                        # Docker configuration
│   ├── frontend/                  # Frontend Docker files
│   ├── backend/                   # Backend Docker files
│   └── postgres/                  # PostgreSQL Docker files
├── docker-compose.yml             # Docker Compose configuration
└── README.md                      # Project documentation
```
