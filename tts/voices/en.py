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
from tensorflow_tts.inference import AutoProcessor
from tensorflow_tts.inference import TFAutoModel

from .voice import Voice

class EnglishVoice(Voice):
  def __init__(self) -> None:
    super().__init__(
      lang = 'en',
      text2mel_model = TFAutoModel.from_pretrained('tensorspeech/tts-tacotron2-ljspeech-en', name='tacotron2'),
      vocoder_model = TFAutoModel.from_pretrained('tensorspeech/tts-melgan-ljspeech-en', name='melgan'),
      processor = AutoProcessor.from_pretrained('tensorspeech/tts-tacotron2-ljspeech-en'),
      special_chars = {
        '°C': 'degrees Celsius',
        '°F': 'degrees Fahrenheit',
        '%': 'percent',
        '€': 'euros',
        '$': 'dollars',
        '£': 'pounds sterling',
        '¥': 'yen',
        '₹': 'rupees',
        '¢': 'cents',
        '§': 'section',
        '©': 'copyright',
        '®': 'registered trademark',
        '™': 'trademark',
        '‰': 'per mille',
        'µ': 'micro',
        '×': 'multiplied by',
        '÷': 'divided by',
        '≠': 'not equal to',
        '≈': 'approximately',
        '+': 'plus',
        '*': 'multiplied by',
        '/': 'divided by',
        '<': 'less than',
        '>': 'greater than',
        '=': 'equal to',
        '≤': 'less than or equal to',
        '≥': 'greater than or equal to',
        '∑': 'sum of',
        '∆': 'delta',
        '∞': 'infinity',
        '√': 'square root of',
        '∫': 'integral of',
        '∂': 'partial',
        '∏': 'product of',
        '∀': 'for all',
        '∈': 'belongs to',
        '∉': 'does not belong to',
        '∅': 'empty set',
      },
    )
