from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

from .voice import Voice

class EnglishVoice(Voice):
  def __init__(self) -> None:
    super().__init__(
      lang = 'en',
      text2mel_model = TFAutoModel.from_pretrained("tensorspeech/tts-tacotron2-ljspeech-en", name="tacotron2"),
      vocoder_model = TFAutoModel.from_pretrained("tensorspeech/tts-melgan-ljspeech-en", name="melgan"),
      processor = AutoProcessor.from_pretrained("tensorspeech/tts-tacotron2-ljspeech-en"),
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
