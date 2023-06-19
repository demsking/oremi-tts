import tensorflow as tf


class Voice:
  def __init__(self, text2mel_model, vocoder_model, processor) -> None:
    self.text2mel_model = text2mel_model
    self.vocoder_model = vocoder_model
    self.processor = processor
    self.text2mel_name = 'TACOTRON'
    self.vocoder_name = 'MB-MELGAN'

  def do_synthesis(self, input_text: str):
    input_ids = self.processor.text_to_sequence(input_text)

    # text2mel part
    if self.text2mel_name == "TACOTRON":
      _, mel_outputs, stop_token_prediction, alignment_history = self.text2mel_model.inference(
          tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
          tf.convert_to_tensor([len(input_ids)], tf.int32),
          tf.convert_to_tensor([0], dtype=tf.int32)
      )
    else:
      raise ValueError("Only TACOTRON, FASTSPEECH2 are supported on text2mel_name")

    # vocoder part
    if self.vocoder_name == "MB-MELGAN":
      # tacotron-2 generate noise in the end symtematic, let remove it :v.
      if self.text2mel_name == "TACOTRON":
        remove_end = 1024
      else:
        remove_end = 1
      audio = self.vocoder_model.inference(mel_outputs)[0, :-remove_end, 0]
    else:
      raise ValueError("Only MB_MELGAN are supported on vocoder_name")

    if self.text2mel_name == "TACOTRON":
      return mel_outputs.numpy(), alignment_history.numpy(), audio.numpy()
    else:
      return mel_outputs.numpy(), audio.numpy()
