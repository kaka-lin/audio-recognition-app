# Audio Recognition

Generating text of the audio file.

![](images/demo.png)

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

### Using through command line interface (CLI)

- #### For WAV File

    ```bash
    $ python audio_recognition.py -f <wav file>
    ```

- #### For MP3 File

    We need to convert `mp3` to `wav`, so we need to use `-c` argument.

    ```bash
    $ python audio_recognition.py -f <mp3 file> -c
    ```

### Using through web application (made with `Gradio`)

```bash
$ python3 audio_recognition_app.py
```

![](images/result.png)
