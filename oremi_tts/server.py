import io
import logging

from flask import Flask, Response, render_template, request
from flask_cors import CORS

from oremi_tts.utils import (
  convert_numbers_to_words,
  save_wav,
  strip_ending_punctuations,
)
from oremi_tts.voices.en import EnglishVoice
from oremi_tts.voices.fr import FrenchVoice

app = Flask('oremi-tts')
voices_instances = {}
voices_objects = {
  'fr': FrenchVoice,
  'en': EnglishVoice,
}

CORS(app)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)


class VoiceNotFound(Exception):
  pass


def load_voice(voice: str):
  if voice not in voices_instances:
    if voice in voices_objects:
      voices_instances[voice] = voices_objects[voice]()
    else:
      raise VoiceNotFound(f'Voice {voice} not found')


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/voices')
def api_get_voices():
  return list(voices_objects.keys())


@app.route('/voice', methods = ['PUT'])
def api_load_voice():
  voice = request.json.get('voice', '').strip()

  if voice:
    try:
      load_voice(voice)
    except VoiceNotFound as error:
      return str(error), 404
  else:
    return 'Bad Request', 400


@app.route('/tts', methods = ['POST'])
def api_tts():
  text = request.json.get('text', '').strip()
  voice = request.json.get('voice', '').strip()
  text = strip_ending_punctuations(text)

  if not voice or not text:
    return 'Bad Request', 400

  try:
    load_voice(voice)
  except VoiceNotFound as error:
    return str(error), 404

  model = voices_instances[voice]
  text = model.parse_special_chars(text)
  text = convert_numbers_to_words(text, lang = model.lang)

  app.logger.info('Synthetizing: %s', text)

  _mels, _alignment_history, audio = model.do_synthesis(text)

  with io.BytesIO() as out:
    save_wav(audio, rate = 24000, path = out)
    return Response(out.getvalue(), mimetype = 'audio/wav')
