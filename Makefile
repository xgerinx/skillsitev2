SHELL := /bin/bash

OS=$(shell uname)

PROJECT_SRC= $(PWD)/src
PROJECT_SQL_FILE= $(PWD)/data/db
PROJECT_INFRASTRUCTURE= $(PWD)/docker

include ${PROJECT_INFRASTRUCTURE}/.env

USER_UID=$(shell id -u)
USER_GID=$(shell id -g)

# set docker build environment based on env variable DOCKER_BUILD_ENVIRONMENT
DOCKER_COMPOSE_FILES=-f ${PROJECT_INFRASTRUCTURE}/docker-compose.yml
ifeq (${DOCKER_BUILD_ENVIRONMENT},DEV)
    ifeq (${OS},Darwin)
        DOCKER_COMPOSE_FILES=-f ${PROJECT_INFRASTRUCTURE}/docker-compose.yml  -f ${PROJECT_INFRASTRUCTURE}/docker-compose.dev.yml
    else
        DOCKER_COMPOSE_FILES=-f ${PROJECT_INFRASTRUCTURE}/docker-compose.yml  -f ${PROJECT_INFRASTRUCTURE}/docker-compose.dev.yml
    endif
else ifeq (${DOCKER_BUILD_ENVIRONMENT},PROD)
    DOCKER_COMPOSE_FILES=-f ${PROJECT_INFRASTRUCTURE}/docker-compose.yml
else ifeq (${DOCKER_BUILD_ENVIRONMENT},TEST)
    DOCKER_COMPOSE_FILES=-f ${PROJECT_INFRASTRUCTURE}/docker-compose.yml -f ${PROJECT_INFRASTRUCTURE}/docker-compose.test.yml
endif


help:
	@echo ""
	@echo "usage: make COMMAND"
	@echo ""
	@echo "Application commands:"
	@echo "====================="
	@echo "  app-build-start            Build and start docker containers"
	@echo "  app-rebuild-start          Destroy, build and start docker containers"
	@echo "  app-install-requirements   Install python requirements from requirements.txt"
	@echo "  app-npm-install            Run npm install as root inside reactify-ui in django container"
	@echo "  app-npm-build            	Build statics for reactify-ui and copy it to target folder"
	@echo "  app-destroy                Destroy docker containers and related data"
	@echo "  app-start                  Start docker containers"
	@echo "  app-stop                   Stop docker containers"
	@echo "  app-restart                Stop and start"
	@echo "  app-logs                   Show application logs (not docker ones!)"
	@echo "  app-cli                    Run command inside django container. Usage: make app-cli param=\"help\"."
	@echo "  app-migrate                Apply django migrations."
	@echo "  app-manage                 Exec django manage command. E.g. make app-manage param=createsuperuser"
	@echo "  app-shell                  Ssh to django container"
	@echo "  app-shell-root             Ssh to django container as root"
	@echo "  app-test                   Run app tests. To add arguments you can use ARGS, e.g. make ARGS='--tags problem' app-functionaltest"
	@echo ""
	@echo ""
	@echo "Docker commands:"
	@echo "====================="
	@echo "  docker-status              Show running status of the docker containers."
	@echo "  docker-logs                Show logs of the docker containers."
	@echo "  docker-container-logs      Show logs of the docker given container: make docker-container-logs container=\"docker-container-name\""
	@echo "  docker-cli                 Execute a bash command on the given container: make docker-cli container=\"docker-container-name\" command=\"ls -la\""
	@echo "  docker-cli-root            Execute a bash command as root on the given container: make docker-cli container=\"docker-container-name\" command=\"ls -la\""
	@echo "  docker-config              Show docker container config"
	@echo ""
	@echo ""


#####################
### APP commands
#####################
app-build-start: docker-build-start app-install-requirements app-migrate app-npm-install app-npm-build


app-destroy: docker-destroy


app-rebuild-start: app-destroy app-build-start


app-start: docker-start app-migrate


app-stop: docker-stop


app-restart: app-stop app-start


app-logs:
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -u ${USER_UID} -T ${DJANGO_SERVICE} tail -f /var/log/django


app-install-requirements:
	@echo "Installing requirements ..."
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -u root -T ${DJANGO_SERVICE} pip install -r requirements.txt

# app-pre-copy-configs:
# 	@cp requirements.txt docker/django/
# 	@cp src/reactify-ui/package.json docker/django/

app-cli:
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -u $(USER_UID) -T ${DJANGO_SERVICE} $(param)

app-migrate:
	@echo "Applying migrations ..."
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -u root -T ${DJANGO_SERVICE} python manage.py migrate

app-test:
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -u root -T ${DJANGO_SERVICE} python manage.py test

app-shell:
	@docker-compose ${DOCKER_COMPOSE_FILES} exec  -u $(USER_UID) ${DJANGO_SERVICE} bash

app-shell-root:
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -u root ${DJANGO_SERVICE} bash

app-shell-redis:
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -u root redis bash

app-npm-install:
	@echo "Installing node modules ..."
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -w /code/reactify-ui -u $(USER_UID) -T ${DJANGO_SERVICE} npm install

app-npm-build:
	@docker-compose ${DOCKER_COMPOSE_FILES} exec -w /code/reactify-ui -u $(USER_UID) -T ${DJANGO_SERVICE} npm run collect

app-manage:
	@docker-compose ${DOCKER_COMPOSE_FILES} exec  -u $(USER_UID) ${DJANGO_SERVICE} python manage.py $(param)

#####################
### DOCKER
#####################
docker-init:
	@if [ -z  $(shell docker ps -a -q) ]; then  \
		  echo "No docker container is running.";  \
	else  \
		  docker stop $(shell docker ps -a -q);  \
	fi


docker-build:
	@docker-compose ${DOCKER_COMPOSE_FILES} build


docker-build-start: docker-build docker-start


docker-destroy:
	@docker-compose ${DOCKER_COMPOSE_FILES} down --remove-orphans -v


docker-images-destroy:
	@docker-compose ${DOCKER_COMPOSE_FILES} down --rmi all


docker-rebuild-start: docker-destroy docker-build-start


docker-start:
	@docker-compose ${DOCKER_COMPOSE_FILES} up


docker-stop:
	@docker-compose ${DOCKER_COMPOSE_FILES} stop


docker-restart: docker-stop docker-start


docker-status:
	@docker ps
	@echo
	@echo '================================================='
	@echo 'DOCKER-SERVICE NAME'
	@docker-compose ${DOCKER_COMPOSE_FILES} config --service


docker-logs:
	@docker-compose ${DOCKER_COMPOSE_FILES} logs -f


docker-container-logs:
	@docker logs -f $(container)
#	@docker-compose ${DOCKER_COMPOSE_FILES} logs -f ${service}

docker-cli:
	@docker exec -u $(USER_UID) -it $(container) ${command}
#	@docker-compose ${DOCKER_COMPOSE_FILES} exec -u $(USER_UID) -T ${service} ${command}


docker-cli-root:
	@docker exec -it $(container) ${command}
#	@docker-compose ${DOCKER_COMPOSE_FILES} exec -T ${service} ${command}

docker-config:
	@docker-compose ${DOCKER_COMPOSE_FILES} config



.PHONY: help

.EXPORT_ALL_VARIABLES:
