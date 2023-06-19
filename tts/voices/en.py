from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

from .voice import Voice

class EnglishVoice(Voice):
  def __init__(self) -> None:
    super().__init__(
      text2mel_model = TFAutoModel.from_pretrained("tensorspeech/tts-tacotron2-ljspeech-en", name="tacotron2"),
      vocoder_model = TFAutoModel.from_pretrained("tensorspeech/tts-melgan-ljspeech-en", name="melgan"),
      processor = AutoProcessor.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr"),
    )
