#!/usr/bin/make -f

# Shamelessly based off @rw_grim's python makefile configuration, without
# whom my knowledge of make and shell scripting would still consist of tears
# and therapy

REQUIREMENTS = \
	requirements.txt \
	requirements-testing.txt \

DB_MIGRATION_COMMAND ?= alembic upgrade head
DB_PATH ?= db.sqlite3
DB_CONNECTION_STRING ?= sqlite:///$(DB_PATH)

MIGRATIONS_DIR ?= migrations

PYTHON_BIN ?= python3
PYTHONPATH ?= $(shell pwd)/src

TEST_DIR ?= test
TEST_OPTIONS ?= -vv --junitxml=junit.xml --cov-report term-missing --cov=src

VENV_BIN ?= virtualenv
VENV_PATH ?= venv
VENV_ACTIVATE = $(VENV_PATH)/bin/activate

.PHONY: all migrate run virtualenv clean clean-pyc 

all: lint check migrate

lint: virtualenv
	. $(VENV_ACTIVATE) ; flake8 --config tox.ini --statistics --count $(LINT_OPTIONS)

check: virtualenv lint $(EXTRA_CHECKS)
	. $(VENV_ACTIVATE) ; PYTHONPATH=$(PYTHONPATH) py.test $(TEST_OPTIONS) --color=auto $(TEST_DIR)

run-daemon: virtualenv migrate
	. $(VENV_ACTIVATE) ; PYTHONPATH=$(PYTHONPATH) python src/daemon.py

run-reprocessor: virtualenv migrate
	. $(VENV_ACTIVATE) ; PYTHONPATH=$(PYTHONPATH) python src/reprocessor.py

migrate: virtualenv
	. $(VENV_ACTIVATE) ; $(DB_MIGRATION_COMMAND)

virtualenv: $(VENV_ACTIVATE)

$(VENV_ACTIVATE): $(REQUIREMENTS)
	test -f $(VENV_PATH)/bin/$(PYTHON_BIN) || $(VENV_BIN) --no-site-packages --python=$(PYTHON_BIN) $(VENV_PATH)
	. $(VENV_ACTIVATE); pip install -U pip
	. $(VENV_ACTIVATE); echo $(REQUIREMENTS) | xargs -n 1 pip install -r
	touch $@

clean: clean-pyc
	rm -rf build dist
	rm -rf *.egg-info
	rm -f junit.xml
	rm -rf $(VENV_PATH)
	rm -f $(DB_PATH)

clean-pyc:
	find $(PYTHONPATH) $(MIGRATIONS_DIR) -iname "*.pyc" -type f | xargs -n 10 rm -f
	find $(PYTHONPATH) $(MIGRATIONS_DIR) -name __pycache__ -type d | xargs -n 10 rm -rf