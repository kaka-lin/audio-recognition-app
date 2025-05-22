import mlx_whisper
from .base import ASRBackend


class MLXWhisperBackend(ASRBackend):
    def __init__(self, model_size="base", language="auto"):
        super().__init__(language, model_size)

    def transcribe(self, audio_path: str) -> str:
        result = mlx_whisper.transcribe(
            audio_path,
            language=self.language, 
            path_or_hf_repo=self.model_size,)
        subtitle_text = result["text"].strip()
        return subtitle_text
