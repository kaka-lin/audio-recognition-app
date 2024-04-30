import gradio as gr
from transformers import pipeline


model = pipeline("automatic-speech-recognition")


def transcribe_audio(mic=None, file=None):
    if mic is not None:
        audio = mic
    elif file is not None:
        audio = file
    else:
        return "You must either provide a mic recording or a file"
    transcription = model(audio)["text"]
    return transcription


app = gr.Interface(
        fn=transcribe_audio,
        inputs=[
            gr.Audio(sources="microphone", type="filepath"),
            gr.Audio(sources="upload", type="filepath"),
        ],
        outputs="text",
    )


if __name__ == "__main__":
    app.launch()
