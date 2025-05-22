from backends import get_backend


def resolve_model_name(backend: str, model_size: str) -> str:
    if backend == "transformers":
        return f"openai/whisper-{model_size}"
    elif backend == "speech-recognition":
        return None
    return model_size


def transcribe_audio(mic, file, backend, language, model_size):
    audio = mic or file
    if audio is None:
        return "請錄音或上傳音訊檔案"
    model_name = resolve_model_name(backend, model_size)
    kwargs = {"language": language}
    if model_name:
        kwargs["model_size"] = model_name
    asr = get_backend(backend, **kwargs)
    return asr.transcribe(audio)
