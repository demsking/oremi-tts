# Oremi Text to Speech

[![Buy me a beer](https://img.shields.io/badge/Buy%20me-a%20beer-1f425f.svg)](https://www.buymeacoffee.com/demsking)

![Oremi Text to Speech Screenshot](screenshot.png)

## Start

**Start Oremi TTS with CPU image**

```sh
docker run -d \
  --name oremi-tts \
  -p 5215:5215 \
  -v ~/.cache/nltk_data:/home/mandela/nltk_data \
  -v ~/.cache/tensorflow_tts:/home/mandela/.cache/tensorflow_tts \
  demsking/oremi-tts
```
For testing, open http://localhost:5215

**Start Oremi TTS with GPU image**

```sh
docker run -d \
  --name oremi-tts \
  --runtime=nvidia \
  -p 5215:5215 \
  -v ~/.cache/nltk_data:/home/mandela/nltk_data \
  -v ~/.cache/tensorflow_tts:/home/mandela/.cache/tensorflow_tts \
  demsking/oremi-tts:gpu-latest
```

For testing, open http://localhost:5215

## Oremi TTS API

Found OpenAPI specification file for Oremi TTS API:

- [Oremi TTS API](https://gitlab.com/demsking/oremi-tts/blob/main/api.yaml)

## License

Under the MIT license.
See [LICENSE](https://gitlab.com/demsking/oremi-tts/blob/main/LICENSE)
file for more details.
