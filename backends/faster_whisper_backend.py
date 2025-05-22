import torch
from faster_whisper import WhisperModel
from .base import ASRBackend


class FasterWhisperBackend(ASRBackend):
    def __init__(self, model_size="base", device="cpu", compute_type="float32", language="auto"):
        super().__init__(language, model_size)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if self.device == "cuda" else "int8"

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe(self, audio_path: str) -> str:
        segments, info = self.model.transcribe(
            audio_path,
            language=self.language,
            beam_size=5,
        )
        return "".join([seg.text for seg in segments])
