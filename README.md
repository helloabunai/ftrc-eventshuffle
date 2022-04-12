# Futurice Eventshuffle API

## Simple instructions

```
## (un)comment appropriate lines in makefile to ensure Production use
git clone git@github.com:helloabunai/ftrc-eventshuffle.git && cd ftrc-eventshuffle
make dcompose-start
make dseed-prod-db
make run-tests
```

A server will be running at http://localhost:6925/. Good to go!

## Detailed description

An EventShuffle implementation in a scalable Flask API, served in a docker container, for Futurice.
As this is a backend task, there is no direct front-end interface included.

The interface/API endpoints were tested and developed by interacting via `curl` and Postman (https://www.postman.com/downloads/).
Requests are expected to be `Content-Type: application/json` with appropriate functions to ensure this is the case.

## Prerequisites

    - Python3 (Developed and tested with 3.8, installs this within container)
    - Docker (whether Docker Desktop, or otherwise. As long as Docker Engine is running!)
    - Docker container details:
        - PYPI Packages
           - Flask==2.1.1
           - Flask-SQLAlchemy==2.5.1
           - gunicorn==20.1.0
           - psycopg2-binary==2.8.6
           - pytest==7.1.1
           - jsonschema==4.4.0
        - Gunicorn (auto build+run)
        - PostgreSQL (auto build+run)
        - NGINX (auto build+run)
    - Unix (Developed on Windows 10 WSL2 CentOS, but also tested on MacOS Monterey)

I have decided to specify exact versions of python dependencies, so that we can replicate environment behaviour exactly between buildtime. This is incase a newer version of any package is released between the time of me writing this, and users testing/using the software, which may result in certain package functions changing behaviour/data-types/returns/etc. Naturally, data types are tested for to ensure things should proceed; I am just being careful and wanting to replicate the experience in it's entirety.

## Running the application

### General information

Before we begin, it is worth noting that environment files should not be stored in version control, and the only reason they are stored in this one is for the complete portability and functionality replication of the Docker container, so that the API can function by those at futurice, as intended :)

First, ensure which environment target you want to build for (development, or production) by uncommenting the required lines. Development will use the Flask built in development web server, whereas production uses a proper WSGI server (gunicorn) and possesses more strict built rules and code standards.

```
## UNCOMMENT FOR PRODUCTION
# ENV_FILE = $(shell pwd)$(shell echo '/.env.prod')
# export $(shell sed 's/=.*//' `pwd`/.env.prod)
# COMPOSE_FILE = $(shell pwd)$(shell echo '/docker-compose.prod.yml')
# DATABASE_STR = "futurice_shuffledb_prod"

## UNCOMMENT FOR DEVELOPMENT
ENV_FILE = $(shell pwd)$(shell echo '/.env.dev')
export $(shell sed 's/=.*//' `pwd`/.env.dev)
COMPOSE_FILE = $(shell pwd)$(shell echo '/docker-compose.yml')
DATABASE_STR = "futurice_shuffledb"
```

Once you have chosen production, or development, the instructions differ very slightly.

---
**NOTE**

It is important to note that you must run the command `make dcompose-wipe` when switching between the two different environments. If you don't wipe the containers, then leftover components may cause linkage issues.

---

#### Development

Starting from scratch:

```
git clone git@github.com:helloabunai/ftrc-eventshuffle.git && cd ftrc-eventshuffle
make dcompose-start
make dseed-dev-db
make run-tests
```

This will launch the Flask development webserver at *http://localhost:5000*, with which you can probe the database via API endpoints. The database will be populated with dummy data, to mimic what was described in the instructions. Additional data can be added, and the application is fault tolerant.

The specification requirement of data being persistent between application launches *does not apply* to the development server, as it is for development. For this behaviour, you need to run the production server, which has data persistence as requested.

#### Production

Starting from scratch:

```
git clone git@github.com:helloabunai/ftrc-eventshuffle.git && cd ftrc-eventshuffle
make dcompose-start
make run-tests
```

---
**NOTE**

Running `run-tests` wipes the database, and inserts the original dummy data, as it is intended to be ran immediately after launching the production container to ensure functionality is at 100%, before serving clients. If you launch the production server, add extra non-default data, then run tests afterwards, this additional data will be lost.

Also, as per news this week (11th April) of a new NGINX vulnerability (https://therecord.media/f5-investigating-reports-of-nginx-zero-day/), it is worth noting that if this was a proper customer based product, different steps would be need to be taken in order to ensure service security.

---

This will launch the production NGINX/Gunicorn web server at *http://localhost:6925*. The production server is data-persistent between reboots of the container. Assuming the production container is currently running from previous commands, test the data persistence by reading the section below.

### Using the software

From the running server, either development or production, the API endpoints are as per the instructions:

 - /api/v1/event/list [GET]
 - /api/v1/event [POST]
 - /api/v1/event/{id} [GET]
 - /api/v1/event/{id}/vote [POST]
 - /api/v1/event/{id}/results [GET]

Using the incorrect request method on any endpoint will return an error.

For the two endpoints that accept POST requests, any json data sent in the body of said POST request will be checked against a json schema to ensure data is in the correct format and of the correct type, before inserting anything into the database. If json fails validation, then an error code will return to the user.

Along with standard checks, such as JSON input validation, as these endpoints take user-input, extra checks are carried out to ensure fault tolerance. Some examples are:
- Check the user adding votes exists *note1
- Check the event ID in the URL given exists
- Check the received, validated vote, does not already exist (no double votes per event)

*note1: As per the specification, the only identifier provided when creating a vote is "name". This was a bit strange to me, as typically names are not unique. However, since this is what the specification called for, names are unique in this database and as such are checked as an identifier when a POST request for adding votes is received. Normally, the end user will not know their database table entry ID, and I am not suggesting this should be expected in the input for votes; if I were to do this "my way", the vote input JSON should include requirements of name, email, phonenumber fields, as these would reliably identify a specific user.

### Data persistence in the production server

In order to test data persistance between container "power cycles", then run raw docker commands (i.e. don't use any commands in the makefile).

```
## add some non-default data via API (e.g. adding a vote)
docker-compose -f docker-compose.prod.yml down 
docker-compose -f docker-compose.prod.yml up
## check added data is still there via API requests or via make dcheck-db
```

Alternatively, if your personal docker settings have launched the container into a tail -f type "live log" window:

```
## add some non-default data via API (e.g. adding a vote)
CTRL+C to quit
docker-compose -f docker-compose.prod.yml up
## check added data is still there via API requests or via make dcheck-db
```

The non-default data that you added to the database will be present throughout container up/down cycles.

## Application tree and description

Below you can find the detailed tree of the application/repository directory, with some explanations of what files do next to them.

```
ftrc-eventshuffle                       # The software
│
├── Makefile                            # Makefile for easy docker/db commands
├── README.md                           # This file :)
├── docker-compose.prod.yml             # Docker-compose for production setting
├── docker-compose.yml                  # Docker-compose for development
└── services                            # All services provided 
    ├── api                             # The API service
    │   ├── Dockerfile                  # Dockerfile for development
    │   ├── Dockerfile.prod             # Dockerfile for production
    │   ├── manage.py                   # Contains functions for the CLI i.e entry from docker
    │   ├── project                     
    │   │   ├── __init__.py
    │   │   ├── app.py                  # The Flask App
    │   │   ├── common                  # Common functions used throughout the project
    │   │   │   ├── database.py
    │   │   │   ├── exceptions.py
    │   │   │   └── validator.py        # Ensures JSON within POST conforms to schemas
    │   │   ├── config.py               # Some environment variables for Flask
    │   │   ├── conftest.py             # PyTest configuration
    │   │   ├── control                 # Control logic
    │   │   │   ├── backend.py          # Where results are calculated/data is gathered
    │   │   │   ├── models.py           # ORM models for PSQL data
    │   │   │   └── views.py            # Views that link to API endpoints
    │   │   ├── schemas                 # POST JSON Body Schemas
    │   │   │   ├── event.json          # For creating a new event
    │   │   │   └── event_vote.json     # For voting on an existing event
    │   │   └── tests
    │   │       ├── test_app.py         # Test API endpoints
    │   │       ├── test_db.py          # Test database and table relations
    │   │       └── test_models.py      # Unit tests for model objects
    │   ├── psql_init.sh                # Ensure PSQL is up before creating Flask (dev)
    │   ├── psql_init_prod.sh           # Ensure PSQL is up before creating Flask (prod)
    │   └── requirements.txt            # PYPI dependencies
    └── nginx                           # The production webserver
        ├── Dockerfile
        └── nginx.conf
```
