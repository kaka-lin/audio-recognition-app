import gradio as gr
from transformers import pipeline


asr = pipeline(
    task="automatic-speech-recognition",
    model="openai/whisper-small",
    device=-1,  # 若使用 GPU，否則改為 -1 表示 CPU
    # 這裡可以選擇使用 TensorFlow 或 PyTorch
    framework="pt",  # "tf" for TensorFlow, "pt" for PyTorch
)


def transcribe_audio(mic, file):
    audio = mic or file
    if audio is None:
        return "請錄音或上傳音訊檔案"
    transcription = asr(audio)["text"]
    return transcription


with gr.Blocks() as app:
    gr.Markdown("## Whisper 語音轉文字")

    with gr.Row():
        mic_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ 麥克風錄音")
        file_input = gr.Audio(sources=["upload"], type="filepath", label="📂 上傳音訊檔")

    output_text = gr.Textbox(label="📝 轉錄結果")

    submit_btn = gr.Button("轉換")
    submit_btn.click(fn=transcribe_audio, inputs=[mic_input, file_input], outputs=output_text)


if __name__ == "__main__":
    # Launch the app
    # Gradio defaults to localhost:7860
    # To create a public link, set share=True
    app.launch()
