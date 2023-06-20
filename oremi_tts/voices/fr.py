from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

from .voice import Voice

class FrenchVoice(Voice):
  def __init__(self) -> None:
    super().__init__(
      lang = 'fr',
      text2mel_model = TFAutoModel.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr", name="tacotron2"),
      vocoder_model = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-synpaflex-fr", name="mb_melgan"),
      processor = AutoProcessor.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr"),
      special_chars = {
        '°C': 'degrés Celsius',
        '°F': 'degrés Fahrenheit',
        '%': 'pour cent',
        '€': 'euros',
        '$': 'dollars',
        '£': 'livres sterling',
        '¥': 'yens',
        '₹': 'roupies',
        '¢': 'centimes',
        '§': 'paragraphe',
        '©': 'copyright',
        '®': 'marque déposée',
        '™': 'marque commerciale',
        '‰': 'pour mille',
        'µ': 'micro',
        '×': 'multiplié par',
        '÷': 'divisé par',
        '≠': 'différent de',
        '≈': 'environ',
        '+': 'plus',
        '*': 'multiplié par',
        '/': 'divisé par',
        '<': 'inférieur à',
        '>': 'supérieur à',
        '=': 'égal à',
        '≤': 'inférieur ou égal à',
        '≥': 'supérieur ou égal à',
        '∑': 'somme de',
        '∆': 'delta',
        '∞': 'infini',
        '√': 'racine carrée de',
        '∫': 'intégrale de',
        '∂': 'partiel',
        '∏': 'produit de',
        '∀': 'pour tout',
        '∈': 'appartient à',
        '∉': 'n\'appartient pas à',
        '∅': 'ensemble vide',
      },
    )
