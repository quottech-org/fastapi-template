PROJECT_NAME ?= ub_back
VERSION = $(shell python3.9 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= q0tik
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

all:

	@echo "make run                              - Create & run development environment in terminal (realtime)"
	@echo "make clean                            - Clean docker volumes"
	@echo "make stop                             - Stops docker containers and delete them"
	@echo "make clean_images                     - Clean docker images"
	@echo "make migrate                          - Alembic migrate"
	@echo "make migrate_test                     - Alembic migrate database_test"
	@echo "make downgrade                        - Alembic downgrade -1"
	@echo "make downgrade_test                   - Alembic downgrade database_test -1"
	@echo "make gen_migrate m=Name_somthing      - Alembic make migrations file"
	@echo "make test n=test_module:test_func     - Run pytest"
	@echo "make sample_fx                        - Run script Sample Bike"
	@exit 0

_clean_makefile:
	rm -fr *.egg-info dist

clean_db:

_down_docker_dev:
	docker-compose -f docker-compose.dev.yml down --remove-orphans

_down_docker_prod:
	docker-compose -f docker-compose.prod.yml down --remove-orphans

clean:
	docker volume prune

run_prod:
	docker-compose -f docker-compose.prod.yml up -d

build_prod:
	docker-compose -f docker-compose.prod.yml build --no-cache

build_dev:
	docker-compose -f docker-compose.dev.yml build --no-cache


test: start_test_docker stop_dev

stop_dev: _down_docker_dev _clean_makefile

run_db:
	docker-compose -f docker-compose.dev.yml up --build -d postgres

start_test_docker:
	docker-compose -f docker-compose.dev.yml run --rm -e SQLALCHEMY_WARN_20=1 -e CONF_PATH=/code/config/config.dev.yml ub_backend pytest -v /code/tests/$$n -x

clean_images:
	docker image prune -a -f

migrate_dev:
	docker-compose -f docker-compose.dev.yml run --rm -e CONF_PATH=/code/config/config.dev.yml ub_backend bash -c "cd ub_backend && alembic upgrade head"

migrate_prod:
	docker-compose -f docker-compose.prod.yml run --rm -e CONF_PATH=/code/config/config.prod.yml ub_backend bash -c "cd ub_backend && alembic upgrade head"

gen_migrate_alembic:
	docker-compose -f docker-compose.dev.yml run --rm ub_backend bash -c "cd ub_backend && alembic revision --autogenerate -m "$$m""

gen_migrate: gen_migrate_alembic


downgrade_dev:
	docker-compose -f docker-compose.dev.yml run --rm -e CONF_PATH=/code/config/config.dev.yml ub_backend bash -c "cd ub_backend && alembic downgrade -1"

downgrade_prod:
	docker-compose -f docker-compose.prod.yml run --rm -e CONF_PATH=/code/config/config.prod.yml ub_backend bash -c "cd ub_backend && alembic downgrade -1"

ls:
	docker-compose -f docker-compose.dev.yml run --rm ub_backend ls -la