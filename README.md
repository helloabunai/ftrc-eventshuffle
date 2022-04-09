# Futurice Eventshuffle API

An EventShuffle implementation in a scalable Flask API, served in a docker container, for Futurice.
As this is a backend task, there is no direct front-end interface included.

The interface/API endpoints were tested and developed by interacting via `curl` and Postman (https://www.postman.com/downloads/).
Requests are expected to be `Content-Type: application/json` with appropriate functions to ensure this is the case.

## Prerequisites

    - Python3 (Developed and tested with 3.8, installs this within container)
    - Docker (which will install these following packages automatically)
        - PYPI Packages
           - Flask==2.1.1
           - Flask-SQLAlchemy==2.5.1
           - psycopg2-binary==2.8.6
        - Gunicorn (auto build+run)
        - PostgreSQL (auto build+run)
    - Unix (Developed on Windows 10 WSL2 CentOS, but also tested on MacOS Monterey)

### Running the development application

Assuming you have docker installed on your local system, then the following instructions are sufficient to deploy
this application. Once you clone the repository, all that is required is to ensure you are in the ./shuffleboard directory, and run the command:

```
docker-compose build
```

This will compose a docker container, which includes a PSQL server for the Flask application to interact with.
Before attempting to interact with any (GET, at least) API endpoints, you will need to populate the database with some data.

You can do this via the following commands (again, from the shuffleboard root directory): 

```
docker-compose exec api python manage.py create_db
docker-compose exec api python manage.py seed_db
```

## Application tree and description

```
├── ftrc-eventshuffle                       # The software
├── Makefile                                # Makefile for easy docker/db commands
├── README.md                               # This file :)
├── docker-compose.prod.yml                 # Docker-compose for production setting
├── docker-compose.yml                      # Docker-compose for development
└── services                                
    └── api                                 # The API service codebase
        ├── Dockerfile                      # Dockerfile for development
        ├── Dockerfile.prod                 # Dockerfile for production
        ├── manage.py                       # Contains functions for the CLI i.e entry from docker
        ├── project
        │   ├── __init__.py
        │   ├── app.py                      # Create Flask APP + link endpoints to views
        │   ├── common                      # Common functions used throughout
        │   │   ├── database.py
        │   │   ├── exceptions.py
        │   │   └── validator.py
        │   ├── config.py                   # App/DB config for Flask app
        │   ├── control                     # Control logic layer
        │   │   ├── backend.py
        │   │   ├── domain.py
        │   │   ├── models.py               # ORM Models for PSQL data
        │   │   └── views.py                # Views that link to API endpoints
        │   ├── schemas                     # Schemas to ensure in/out is valid
        │   │   ├── date.json
        │   │   ├── event.json
        │   │   ├── person.json
        │   │   └── seed_data.json          # Data to populate DB from scratch
        │   └── tests                       # Test suite for pytest
        │       ├── test_database.py
        │       └── test_models.py
        ├── psql_init.sh                    # Ensure PSQL is up before creating Flask (dev)
        ├── psql_init_prod.sh               # Same, but for production
        └── requirements.txt                # PYPI dependencies
```