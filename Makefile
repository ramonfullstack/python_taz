export PYTHONPATH=$PYTHONPATH:$(pwd)
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
MESSAGE=$(shell git log --pretty=format:'%an: %h %s' -1)
UNAME_S := $(shell uname -s)

# Note that this ifeq-endif are space-indented for better readability
ifeq ($(UNAME_S), Linux)
    OPEN_EXECUTABLE ?= xdg-open
endif
ifeq ($(UNAME_S), Darwin)
    OPEN_EXECUTABLE ?= open
endif
OPEN_EXECUTABLE ?= :

test:
	@SIMPLE_SETTINGS=taz.settings.test py.test -s -vv taz -m 'not integration'

test-matching:
	@SIMPLE_SETTINGS=taz.settings.test py.test -rxs -vv --pdb -k$(Q) taz -m 'not integration'

test-integration-matching:
	@SIMPLE_SETTINGS=taz.settings.test py.test -rxs --pdb -k$(Q) taz -m 'integration'

run:
	@./run_helper.sh $(environment) $(jobtype) $(scope) $(generate_binary)

run-consumers-dev:
	@./run_consumers.sh

run-pollers-dev:
	@./run_pollers.sh

run-api:
	@SIMPLE_SETTINGS=taz.settings.development \
	GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} \
	gunicorn taz.api:app --reload

requirements:
	@pip install -r requirements/test.txt --extra-index-url ${PIP_EXTRA_INDEX_URL}

requirements-dev:
	@pip install -r requirements/dev.txt --extra-index-url ${PIP_EXTRA_INDEX_URL}
	@pre-commit install

.PHONY: requirements

run-docs:
	@mkdocs serve

build-docs:
	@mkdocs build --clean

publish-docs:
	@pip install -r requirements/docs.txt
	@pip install awscli==1.11.73
	@mkdocs build --clean
	@aws s3 sync /builds/luizalabs/taz/site s3://luizalabs-docs/taz --acl public-read

test-coverage:
	@SIMPLE_SETTINGS=taz.settings.test py.test -xs --durations=30 --cov taz -m 'not integration' --cov-report xml --cov-report term-missing

coverage-open:
	@SIMPLE_SETTINGS=taz.settings.test py.test -xs --cov taz -m 'not integration' --cov-report html
	$(OPEN_EXECUTABLE) htmlcov/index.html

lint:
	@flake8 .
	@isort . --check

fix-python-import:
	@isort -rc .

check-vulnerabilities:
	safety check -r requirements/production.txt

create-token:
	@SIMPLE_SETTINGS=taz.settings.development python taz/api/commands.py --token=$(token) --owner=$(owner)

create-matching-replica:
	@SIMPLE_SETTINGS=taz.settings.development python create_database_reduced_replica_for_matching_tests.py

release-patch:
	bump2version patch --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | SIMPLE_SETTINGS=taz.settings.test xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bump2version patch

release-minor:
	bump2version minor --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | SIMPLE_SETTINGS=taz.settings.test xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bumpversion minor

release-major:
	bump2version major --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | SIMPLE_SETTINGS=taz.settings.test xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bumpversion major

check-update-requirements:
	pip list --outdated --format=columns

kafka-create-topic:
	@docker exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic test

kafka-list-topics:
	@docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

run-kafka-producer:
	@docker exec --interactive --tty kafka kafka-console-producer --bootstrap-server localhost:9092 --topic test

run-kafka-consumer:
	@docker exec --interactive --tty kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic test --from-beginning
