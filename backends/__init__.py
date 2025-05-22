from .transformers_backend import TransformersBackend
from .speech_recognition_backend import SpeechRecognitionBackend


def get_backend(name: str, **kwargs):
    name = name.lower()
    if name == "transformers":
        return TransformersBackend(**kwargs)
    elif name == "speech-recognition":
        return SpeechRecognitionBackend(**kwargs)
    else:
        raise ValueError(f"Unknown backend: {name}")
