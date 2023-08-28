APP_NAME := $(shell python metadata.py name)
APP_VERSION := $(shell python metadata.py version)
IMAGE_NAME := demsking/$(APP_NAME)

TENSORFLOW_VERSION := 2.9.2

SSL_PATH := ~/.config/oremi/ssl
SSL_CERT_FILE := $(SSL_PATH)/localhost.pem

.PHONY: all images publish-images test

# Start the development environment using tmuxinator
env:
	tmuxinator

install:
	pip install pylint
	pip install --no-cache-dir -r requirements.txt

$(SSL_CERT_FILE):
	mkdir -p $(shell dirname $@)
	openssl req -x509 -nodes -new -sha256 -days 3650 -newkey rsa:2048 \
	  -subj "/C=CM/CN=localhost" \
	  -addext "subjectAltName = DNS:discovery" \
	  -keyout $(SSL_PATH)/localhost-key.pem \
	  -out $(SSL_CERT_FILE)

certificates: $(SSL_CERT_FILE)

start: certificates
	docker-compose up

lint:
	pre-commit run --all-files

fix:
	ruff check . --fix

test:
	pytest

coverage:
	pytest --cov=oremi-tts

coverage-html:
	pytest --cov=oremi-tts --cov-report=html

update:
	nix flake update
	pre-commit autoupdate

images:
	docker build \
	  --progress plain . -t $(IMAGE_NAME):$(APP_VERSION) \
	  --build-arg TENSORFLOW_VERSION="$(TENSORFLOW_VERSION)" \
	  --build-arg PACKAGE_NAME="$(APP_NAME)" \
	  --build-arg CREATED_DATE="$(shell date --rfc-3339=seconds)" \
	  --build-arg MAINTAINER="$(shell python metadata.py authors)" \
	  --build-arg DESCRIPTION="$(shell python metadata.py description)" \
	  --build-arg DOCUMENTATION="$(shell python metadata.py documentation)" \
	  --build-arg VERSION="$(APP_VERSION)" \
	  --build-arg REVISION="$(shell git rev-parse HEAD)" \
	  --build-arg SOURCE_URL="$(shell python metadata.py repository)" \
	  --build-arg VENDOR="Sébastien Demanou" \
	  --build-arg LICENSE="$(shell python metadata.py license)"
	docker tag $(IMAGE_NAME):$(APP_VERSION) $(IMAGE_NAME):latest
	docker build \
	  --progress plain . -t $(IMAGE_NAME):$(APP_VERSION)-gpu \
	  --build-arg TENSORFLOW_VERSION="$(TENSORFLOW_VERSION)-gpu" \
	  --build-arg PACKAGE_NAME="$(APP_NAME)" \
	  --build-arg CREATED_DATE="$(shell date --rfc-3339=seconds)" \
	  --build-arg MAINTAINER="$(shell python metadata.py authors)" \
	  --build-arg DESCRIPTION="$(shell python metadata.py description)" \
	  --build-arg DOCUMENTATION="$(shell python metadata.py documentation)" \
	  --build-arg VERSION="$(APP_VERSION)" \
	  --build-arg REVISION="$(shell git rev-parse HEAD)" \
	  --build-arg SOURCE_URL="$(shell python metadata.py repository)" \
	  --build-arg VENDOR="Sébastien Demanou" \
	  --build-arg LICENSE="$(shell python metadata.py license)"
	docker tag $(IMAGE_NAME):$(APP_VERSION)-gpu $(IMAGE_NAME):latest-gpu

publish-images: images
	git commit pyproject.toml -m "Release $(APP_VERSION)"
	git tag v$(APP_VERSION)
	docker push $(IMAGE_NAME):$(APP_VERSION)
	docker push $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):$(APP_VERSION)-gpu
	docker push $(IMAGE_NAME):latest-gpu
	git push --tags origin main
