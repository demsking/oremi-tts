from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

from .voice import Voice

class FrenchVoice(Voice):
  def __init__(self) -> None:
    super().__init__(
      text2mel_model = TFAutoModel.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr", name="tacotron2"),
      vocoder_model = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-synpaflex-fr", name="mb_melgan"),
      processor = AutoProcessor.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr"),
    )
