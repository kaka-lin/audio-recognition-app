import speech_recognition as sr

from .base import ASRBackend
from utils.mp3_utils import convert_mp3_to_wav


class SpeechRecognitionBackend(ASRBackend):
    def __init__(self, language="zh"):
        super().__init__(language=language)
        self.recognizer = sr.Recognizer()
    
    def mp3_to_wav(self, audio_path: str) -> str:
        if audio_path.endswith(".mp3"):
            wav_path = audio_path.replace(".mp3", ".wav")
            convert_mp3_to_wav(audio_path, wav_path)
            return wav_path
        return audio_path

    def transcribe(self, audio_path: str) -> str:
        print(self.language)
        audio_path = self.mp3_to_wav(audio_path)
        with sr.AudioFile(audio_path) as source:
            audio = self.recognizer.record(source)
            try:
                return self.recognizer.recognize_google(audio, language=self.language)
            except sr.UnknownValueError:
                return "無法辨識語音內容"
            except sr.RequestError as e:
                return f"無法連接 Google 語音服務：{e}"
