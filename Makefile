IMAGE_VERSION := 1.0.1
TENSORFLOW_VERSION := 2.9.2
IMAGE_NAME := demsking/oremi-tts

IMAGE_FILES := $(wildcard oremi_tts/**/*)
IMAGE_FILES := $(filter-out %/__pycache__%, $(IMAGE_FILES))

.PNONY: lint build-images publish-images

# start dev env
env:
	tmuxinator

lint:
	pre-commit run --all-files

install:
	pip install -r requirements.txt

start:
	python -m oremi_tts

build-images: $(IMAGE_FILES)
	docker build . --build-arg TENSORFLOW_VERSION=$(TENSORFLOW_VERSION) -t $(IMAGE_NAME):$(IMAGE_VERSION) \
		&& docker build . --build-arg TENSORFLOW_VERSION=$(TENSORFLOW_VERSION) -t $(IMAGE_NAME):latest \
		&& docker build . --build-arg TENSORFLOW_VERSION=$(TENSORFLOW_VERSION)-gpu -t $(IMAGE_NAME):$(IMAGE_VERSION)-gpu \
		&& docker build . --build-arg TENSORFLOW_VERSION=$(TENSORFLOW_VERSION)-gpu -t $(IMAGE_NAME):gpu-latest

publish-images: build-images
	git commit . -m "Release $(IMAGE_VERSION)"
	git tag v$(IMAGE_VERSION)
	docker push $(IMAGE_NAME):$(IMAGE_VERSION)
	docker push $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):$(IMAGE_VERSION)-gpu
	docker push $(IMAGE_NAME):gpu-latest
	git push --tags origin main
