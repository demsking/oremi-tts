# Copyright 2023 Sébastien Demanou. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import io

from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask_cors import CORS
from oremi.core.logger import Logger

from .package import APP_NAME
from .utils import convert_numbers_to_words
from .utils import save_wav
from .utils import strip_ending_punctuations
from .voices.en import EnglishVoice
from .voices.fr import FrenchVoice

app = Flask(APP_NAME)
logger = Logger.create(APP_NAME)
voices_instances = {}
voices_objects = {
  'fr': FrenchVoice,
  'en': EnglishVoice,
}

CORS(app)


class VoiceNotFoundError(Exception):
  pass


def load_voice(voice: str):
  if voice not in voices_instances:
    logger.info(f'Loading voice model for {voice}')

    if voice in voices_objects:
      voices_instances[voice] = voices_objects[voice]()
    else:
      logger.error(f'Voice {voice} not found')
      raise VoiceNotFoundError(f'Voice {voice} not found')


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
      return 'Loaded', 200
    except VoiceNotFoundError:
      return 'Voice Not Found', 404
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
  except VoiceNotFoundError:
    return 'Voice Not Found', 404

  logger.info('Decoding: %s', text)

  model = voices_instances[voice]
  text = model.parse_special_chars(text)
  text = convert_numbers_to_words(text, lang = model.lang)

  logger.info('Synthesizing: %s', text)

  _mels, _alignment_history, audio = model.do_synthesis(text) # pylint: disable=unused-variable

  logger.info('Sending audio data')

  with io.BytesIO() as out:
    save_wav(audio, rate = 24000, path = out)
    return Response(out.getvalue(), mimetype = 'audio/wav')
