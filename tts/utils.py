import numpy as np
import scipy.io.wavfile

__all__ = [
  'save_wav',
  'strip_ending_punctuations',
]

_PUNCTUATIONS = [".", ",", "?", "!", ":", ";", "-", "(", ")", "[", "]", "{", "}", "\"", "'", "`", "...", "«", "»", "“", "”", "‘", "’", "–", "—"]


def save_wav(wav, path, rate = 24000):
  wav_norm = (wav * (32767 / max(0.01, np.max(np.abs(wav))))).astype(np.int16)
  scipy.io.wavfile.write(path, rate, wav_norm)


def strip_ending_punctuations(text: str):
  while text[-1] in _PUNCTUATIONS:
    text = text[0:-1].strip()
  return text
