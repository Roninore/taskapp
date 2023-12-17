.PHONY: default venv lint pretty dev-start dev-build prod-rsync prod-stop prod-build prod-migrate prod-stop

default:
	@echo "There is no default target."

venv:
	rm -rf venv
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

lint:
	./venv/bin/black --check -l 79 taskapp
	./venv/bin/flake8 taskapp
	./venv/bin/isort -c --src taskapp --profile black -l 79 taskapp

pretty:
	./venv/bin/black -l 79 taskapp
	./venv/bin/flake8 taskapp
	./venv/bin/isort --src taskapp --profile black -l 79 taskapp

lint-win:
	./venv/Scripts/black --check -l 79 taskapp
	./venv/Scripts/flake8 taskapp
	./venv/Scripts/isort -c --src taskapp --profile black -l 79 taskapp

pretty-win:
	./venv/Scripts/black -l 79 taskapp
	./venv/Scripts/flake8 taskapp
	./venv/Scripts/isort --src taskapp --profile black -l 79 taskapp

dev-start:
	docker-compose -f deployments/docker-compose.dev.yml up --force-recreate --remove-orphans

dev-stop:
	docker-compose -f deployments/docker-compose.dev.yml down

dev-build:
	docker-compose -f deployments/docker-compose.dev.yml build --no-cache

prod-rsync:
	rsync -a --progress --delete --rsync-path=/usr/bin/rsync ./ ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_ROOT}

prod-stop:
	docker-compose -f deployments/docker-compose.prod.yml down

prod-build:
	docker-compose -f deployments/docker-compose.prod.yml build --no-cache

prod-start:
	docker-compose -f deployments/docker-compose.prod.yml up --force-recreate --remove-orphans -d
