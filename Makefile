
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

include $(ENV_FILE)

clear:
	@find . -name __pycache__ -prune -exec rm -rf {} +
	@find . -name "*.pyc" -prune -exec rm -rf {} +
	@find . -name .cache -prune -exec rm -rf {} +

dcompose-start:
	@docker-compose stop;
	@docker-compose -f ${COMPOSE_FILE} up --build;

dcompose-stop:
	@docker-compose stop;

dcompose-wipe:
	@docker-compose down -v --remove-orphans;

dseed-prod-db:
	@docker-compose exec api python /home/app/api/manage.py seed_db;

dseed-dev-db:
	@docker-compose exec api python manage.py seed_db;

dcheck-db:
	@docker-compose exec db psql --username=postgres --db=$(DATABASE_STR);

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
	@echo 'dcompose-wipe:'
	@echo '  Wipes and removes orphans (use when switching between dev/prod).'	
	@echo 'dseed-prod-db:'
	@echo '  Populates the production PSQL database with data to test/interact with.'
	@echo 'dseed-dev-db:'
	@echo '  Populates the development PSQL database with data to test/interact with.'
	@echo 'dcleanup:'
	@echo '  Removes exited containers and images.'
	@echo 'run-tests:'
	@echo '  Runs pytest based testing suite.'