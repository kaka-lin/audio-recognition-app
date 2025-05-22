import platform

from .transformers_backend import TransformersBackend
from .speech_recognition_backend import SpeechRecognitionBackend
from .whisper_backend import WhisperBackend
from .faster_whisper_backend import FasterWhisperBackend


def get_backend(name: str, **kwargs):
    name = name.lower()
    if name == "transformers":
        return TransformersBackend(**kwargs)
    elif name == "speech-recognition":
        return SpeechRecognitionBackend(**kwargs)
    elif name == "whisper":
        return WhisperBackend(**kwargs)
    elif name == "faster-whisper":
        return FasterWhisperBackend(**kwargs)
    elif name == "mlx-whisper" and platform.system() == "Darwin":
        from .mlx_whisper_backend import MLXWhisperBackend
        return MLXWhisperBackend(**kwargs)
    else:
        raise ValueError(f"Unknown backend: {name}")
