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
├── shuffleboard               # The application!
│   ├── services/api
│   │
│   └── ├── project            # API Codebase
│   │       ├── __init__.py    # Initialise + create Flask APP
│   │       ├── models.py      # Store model objects for PSQL DB interface
│   │       ├── views.py       # API endpoint URI's
│   │       └── config.py      # Environment variables
│   │
│   ├── Dockerfile             # Development docker file
│   ├── Dockerfile.prod        # Production docker file
│   │
│   ├── requirements.txt       # PYPI dependencies
│   │
│   ├── psql_init_prod.sh      # PSQL initialise script (production)
│   ├── psql_init.sh           # PSQL initialise script (development)
│   │
│   └── manage.py              # CLI for launching the application
│
├── .env.dev                   # Environment variables
├── .env.prod                  # For normal production products, these would not be stored
├── .env.prod.db               # in repo, but for scope of this; figured ok.
│ 
├── docker-compose.yml         # Docker compose (development)
├── docker-compose.prod.yml    # Docker compose (production)
│
└── README.md                  # This file :)
```