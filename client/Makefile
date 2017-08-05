#!/usr/bin/make -f

# CRA --> create-react-app
CRA_BROWSER ?= none
CRA_HOST ?= 127.0.0.1
CRA_PORT ?= 8081

# it looks like the stock create-react-app rolls linting into the build itself..?

.PHONY: check build clean clean-node

all: requirements check build

clean:
	rm -rf build
	rm -rf coverage
	rm -rf testrattingcapitals.com

clean-node:
	rm -rf node_modules

requirements:
	yarn

check: requirements
	npm run test -- --coverage

check-watch: requirements
	npm run test

build: requirements check
	npm run build

run-client: requirements
	# prevent foot-gunning by refusing to start if the API server isn't alive
	curl -m 1 --silent --output /dev/null -f http://localhost:8080/health || (echo "API server isn't running!" && exit 1)
	BROWSER=$(CRA_BROWSER) HOST=$(CRA_HOST) PORT=$(CRA_PORT) npm run start

deploy: clean build
	cp -Rf build testrattingcapitals.com
	rsync -a testrattingcapitals.com tony@testrattingcapitals.com:/var/www/html
	rm -rf testrattingcapitals.com
