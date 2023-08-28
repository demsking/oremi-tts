# Oremi Text to Speech

[![Buy me a beer](https://img.shields.io/badge/Buy%20me-a%20beer-1f425f.svg)](https://www.buymeacoffee.com/demsking)

Oremi Text to Speech leverages TensorflowTTS to convert text into
natural-sounding speech, enabling seamless integration of high-quality
text-to-speech capabilities into applications.

![Oremi Text to Speech Screenshot](https://gitlab.com/demsking/oremi-tts/-/raw/main/screenshot.webp)

## Table of Contents

- [Running the Oremi TTS Service with CPU](#running-the-oremi-tts-service-with-cpu)
- [Running the Oremi TTS Service with GPU](#running-the-oremi-tts-service-with-gpu)
- [Oremi TTS API](#oremi-tts-api)
- [Contribute](#contribute)
- [Versioning](#versioning)
- [License](#license)

## Running the Oremi TTS Service with CPU

Use the official Docker image [`demsking/oremi-tts`](https://hub.docker.com/r/demsking/oremi-tts):

```sh
docker run -d \
  --name oremi-tts \
  -p 5215:5215 \
  -v ~/.cache/nltk_data:/home/oremi/nltk_data \
  -v ~/.cache/tensorflow_tts:/home/oremi/.cache/tensorflow_tts \
  demsking/oremi-tts:latest
```

You can access the Oremi TTS service from your web browser by navigating to
http://localhost:5215. This will open the Oremi TTS user interface, where you can
input text and listen to the generated speech.

## Running the Oremi TTS Service with GPU

Use the official Docker image [`demsking/oremi-tts`](https://hub.docker.com/r/demsking/oremi-tts):

```sh
docker run -d \
  --name oremi-tts \
  --runtime=nvidia \
  -p 5215:5215 \
  -v ~/.cache/nltk_data:/home/oremi/nltk_data \
  -v ~/.cache/tensorflow_tts:/home/oremi/.cache/tensorflow_tts \
  demsking/oremi-tts:latest-gpu
```

You can access the Oremi TTS service from your web browser by navigating to
http://localhost:5215. This will open the Oremi TTS user interface, where you
can input text and listen to the generated speech.

## Oremi TTS API

Found OpenAPI specification file for Oremi TTS API:

- [Oremi TTS API](https://gitlab.com/demsking/oremi-tts/blob/main/openapi.yaml)

## Contribute

Please follow [CONTRIBUTING.md](https://gitlab.com/demsking/oremi-tts/blob/main/CONTRIBUTING.md).

## Versioning

Given a version number `MAJOR.MINOR.PATCH`, increment the:

- `MAJOR` version when you make incompatible API changes,
- `MINOR` version when you add functionality in a backwards-compatible manner,
  and
- `PATCH` version when you make backwards-compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions
to the `MAJOR.MINOR.PATCH` format.

See [SemVer.org](https://semver.org/) for more details.

## License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at [LICENSE](https://gitlab.com/demsking/oremi-tts/blob/main/LICENSE).
