from abc import ABC, abstractmethod


class ASRBackend(ABC):
    def __init__(self, language="auto", model_size=None):
        self.language = None if language == "auto" else language
        self.model_size = model_size

    @abstractmethod
    def transcribe(self, audio_path: str) -> str:
        pass
