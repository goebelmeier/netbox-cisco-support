NETBOX_VER?=v3.0.11

NAME=netbox-cisco-support

COMPOSE_FILE=./develop/docker-compose.yml
OVERRRIDE_COMPOSE_FILE=./develop/docker-compose.override.yml
BUILD_NAME=netbox_cisco_support
VERFILE=./netbox_cisco_support/version.py


cbuild:
	docker-compose -f ${COMPOSE_FILE} \
	    -f ${OVERRRIDE_COMPOSE_FILE} \
		-p ${BUILD_NAME} build \
		--build-arg netbox_ver=${NETBOX_VER}

debug:
	@echo "Starting Netbox .. "
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} up

start:
	@echo "Starting Netbox in detached mode.. "
	docker-compose -f ${COMPOSE_FILE}  -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} up -d

stop:
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} down

destroy:
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} down
	docker volume rm -f ${BUILD_NAME}_pgdata_netbox_cisco_support

nbshell:
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} run --rm netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py nbshell

shell:
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} run --rm netbox shell

adduser:
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} run --rm netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py createsuperuser

collectstatic:
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} run --rm netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py collectstatic

migrations:
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} up -d postgres
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} \
	run --rm netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py makemigrations --name ${BUILD_NAME}
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} down

pbuild:
	python3 -m pip install --upgrade build
	python3 -m build

pypipub:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*

relpatch:
	$(eval GSTATUS := $(shell git status --porcelain))
ifneq ($(GSTATUS),)
	$(error Git status is not clean. $(GSTATUS))
endif
	git checkout develop
	git remote update
	git pull origin develop
	$(eval CURVER := $(shell cat $(VERFILE) | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'))
	$(eval NEWVER := $(shell pysemver bump patch $(CURVER)))
	$(eval RDATE := $(shell date '+%Y-%m-%d'))
	git checkout -b release-$(NEWVER) origin/develop
	echo '__version__ = "$(NEWVER)"' > $(VERFILE)
	git commit -am 'bump ver'
	git push origin release-$(NEWVER)
	git checkout develop


test:
	docker-compose -f ${COMPOSE_FILE} -f ${OVERRRIDE_COMPOSE_FILE} -p  ${BUILD_NAME} run netbox python manage.py test ${BUILD_NAME}
