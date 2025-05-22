from transformers import pipeline
from .base import ASRBackend


class TransformersBackend(ASRBackend):
    def __init__(self, model_name="openai/whisper-small", device=-1, language="auto", model_size=None):
        super().__init__(language)
        self.asr = pipeline(
            task="automatic-speech-recognition",
            model=model_name,
            device=device,   # -1 for CPU, 0 for GPU
            framework="pt",  # "tf" for TensorFlow, "pt" for PyTorch
        )

    def transcribe(self, audio_path: str) -> str:
        return self.asr(audio_path)["text"]
