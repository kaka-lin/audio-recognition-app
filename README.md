# Audio Recognition

Generating text of the audio file.

## Requirements

- Python3+
- pygame
- pydub
- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- [ffmpeg](https://ffmpeg.org/)

## Install

1. Python packages

    ```bash
    $ pip3 install -r requirements.txt
    ```

2. ffmpeg

    ```bash
    # Ubuntu
    $ sudo apt install ffmpeg

    # Mac
    $ brew install ffmpeg
    ```

    For `Windows`, you can refer to this website: [ffmpeg install](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)

## Usage

```bash
$ python audio_recognition.py -f <wav file>

# or

$ python audio_recognition.py -f <mp3 file> -c
```

