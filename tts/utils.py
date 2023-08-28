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
import re

import numpy as np
import scipy.io.wavfile
from num2words import num2words

__all__ = [
  'save_wav',
  'convert_numbers_to_words',
  'strip_ending_punctuations',
]

_PUNCTUATIONS = [
  '.', ',', '?', '!', ':', ';', '-', '(', ')', '[', ']', '{', '}',
  "\"", "'", '`', '...', '«', '»', '“', '”', '‘', '’', '-', '—',
]


def convert_numbers_to_words(text: str, lang: str):
  words = []
  for word in text.split():
    if re.match(r'^-?\d+\.?\d*$', word):
      number = float(word) if '.' in word else int(word)
      number_in_words = num2words(number, lang = lang)
      words.append(number_in_words)
    else:
      words.append(word)
  return ' '.join(words)


def save_wav(wav, path, rate = 24000):
  wav_norm = (wav * (32767 / max(0.01, np.max(np.abs(wav))))).astype(np.int16)
  scipy.io.wavfile.write(path, rate, wav_norm)


def strip_ending_punctuations(text: str):
  while text[-1] in _PUNCTUATIONS:
    text = text[0:-1].strip()
  return text
