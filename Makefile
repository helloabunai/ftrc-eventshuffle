
#ENV_FILE = $(shell pwd)$(shell echo '/.env.prod')
ENV_FILE = $(shell pwd)$(shell echo '/.env.dev')

include $(ENV_FILE)

#export $(shell sed 's/=.*//' `pwd`/.env.prod)
export $(shell sed 's/=.*//' `pwd`/.env.dev)

#COMPOSE_FILE = $(shell pwd)$(shell echo '/docker-compose.prod.yml')
COMPOSE_FILE = $(shell pwd)$(shell echo '/docker-compose.yml')

clear:
	@find . -name __pycache__ -prune -exec rm -rf {} +
	@find . -name "*.pyc" -prune -exec rm -rf {} +
	@find . -name .cache -prune -exec rm -rf {} +

dcompose-start:
	@docker-compose stop;
	@docker-compose -f ${COMPOSE_FILE} build;
	@docker-compose up -d;

dcompose-stop:
	@docker-compose stop

dcreate-db:
	@docker-compose exec api python manage.py create_db;

dseed-db:
	@docker-compose exec api python manage.py seed_db;

dcheck-db:
	@docker-compose exec db psql --username=postgres --db=futurice_shuffledb;

dcleanup:
	@docker rm $(shell docker ps -qa --no-trunc --filter "status=exited")
	@docker rmi $(shell docker images --filter "dangling=true" -q --no-trunc)

run-tests: clear
	@docker-compose exec api python -m pytest -vvv -rP

help:
	@echo 'clear:'
	@echo '  Prunes python bytecode from working directory.'
	@echo 'dcompose-start:'
	@echo '  Stops running containers, re-builds and starts fresh.'
	@echo 'dcompose-stop:'
	@echo '  Stops running docker containers.'
	@echo 'dcreate-db:'
	@echo '  Interacts with manage.py within the container to create DB if it does not exist.'
	@echo '  NOTE: This would be run upon container launch anyway. Exists in makefile for debug.'
	@echo 'dseed-db:'
	@echo '  Populates the PSQL server with data to test/interact with.'
	@echo 'dcheck-db:'
	@echo '  Check PSQL server within running container.'
	@echo 'dcleanup:'
	@echo '  Removes exited containers and images.'
	@echo 'run-tests:'
	@echo '  Runs pytest based testing suite.'