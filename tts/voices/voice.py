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

import tensorflow as tf


class Voice:
  def __init__(self, lang: str, text2mel_model, vocoder_model, processor, special_chars):
    self.lang = lang
    self.text2mel_model = text2mel_model
    self.vocoder_model = vocoder_model
    self.processor = processor
    self.text2mel_name = 'TACOTRON'
    self.vocoder_name = 'MB-MELGAN'
    self.special_chars = special_chars

  def parse_special_chars(self, text: str):
    for special_char, word in self.special_chars.items():
      if special_char in text:
        text = text.replace(special_char, f' {word} ')
    return re.sub(r'\s+', ' ', text)

  def do_synthesis(self, input_text: str):
    input_ids = self.processor.text_to_sequence(input_text)

    # text2mel part
    if self.text2mel_name == 'TACOTRON':
      _, mel_outputs, _stop_token_prediction, alignment_history = self.text2mel_model.inference( # pylint: disable=unused-variable
        tf.expand_dims(tf.convert_to_tensor(input_ids, dtype = tf.int32), 0),
        tf.convert_to_tensor([len(input_ids)], tf.int32),
        tf.convert_to_tensor([0], dtype = tf.int32)
      )
    else:
      raise ValueError('Only TACOTRON, FASTSPEECH2 are supported on text2mel_name')

    # vocoder part
    if self.vocoder_name == 'MB-MELGAN':
      if self.text2mel_name == 'TACOTRON':
        # tacotron-2 generate noise in the end symtematic, let remove it :v.
        remove_end = 1024
      else:
        remove_end = 1
      audio = self.vocoder_model.inference(mel_outputs)[0, :-remove_end, 0]
    else:
      raise ValueError('Only MB_MELGAN are supported on vocoder_name')

    if self.text2mel_name == 'TACOTRON':
      return mel_outputs.numpy(), alignment_history.numpy(), audio.numpy()

    return mel_outputs.numpy(), audio.numpy()
