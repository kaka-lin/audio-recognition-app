import whisper
from .base import ASRBackend


class WhisperBackend(ASRBackend):
    def __init__(self, model_size="base", language="auto"):
        super().__init__(language, model_size)
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path: str) -> str:
        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(
            audio,
            n_mels=self.model.dims.n_mels
        ).to(self.model.device)

        # detect the spoken language
        # _, probs = self.model.detect_language(mel)
        # print(f"Detected language: {max(probs, key=probs.get)}")

        # decode the audio
        options = whisper.DecodingOptions(language=self.language)
        result = whisper.decode(self.model, mel, options)
        subtitle_text = result.text.strip()

        return subtitle_text
