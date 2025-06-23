fastapi_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app instance
│   ├── api/               # Routers/endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints.py
│   ├── core/              # Config, security, etc.
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/            # Pydantic models & DB models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── crud/              # CRUD operations
│   │   ├── __init__.py
│   │   └── user.py
│   ├── db/                # Database session, init, etc.
│   │   ├── __init__.py
│   │   └── session.py
│   └── dependencies/      # Dependency functions
│       ├── __init__.py
│       └── auth.py
│
├── tests/                 # Unit and integration tests
│   └── test_main.py
│
├── requirements.txt
└── README.md