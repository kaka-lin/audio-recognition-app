import argparse

import gradio as gr

from backends import get_backend
from cli import run_cli

backend_choices = ["transformers", "faster-whisper", "whisper", "speech-recognition"]
language_choices = ["zh", "en", "ja", "ko", "auto"]

model_size_options = {
    "transformers": ["tiny", "base", "small", "medium", "large"],
    "faster-whisper": ["tiny", "base", "small", "medium", "large-v2", "large-v3"],
    "whisper": ["tiny", "base", "small", "medium", "large"],
    "speech-recognition": ["google"],
}


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


def update_model_size_dropdown(backend):
    return gr.Dropdown(
        choices=model_size_options[backend],
        value=model_size_options[backend][0],
    )


def build_demo():
    # Create a Gradio interface
    with gr.Blocks() as app:
        # UI parts
        gr.Markdown("## 🧠 Multi-ASR Toolkit - 語音轉文字平台")

        with gr.Row():
            backend_dropdown = gr.Dropdown(choices=backend_choices, label="選擇引擎", value="transformers")
            language_dropdown = gr.Dropdown(choices=language_choices, label="語言", value="auto")
            modelsize_dropdown = gr.Dropdown(
                choices=model_size_options["transformers"],
                label="模型大小",
                value="small"
            )

        with gr.Row():
            mic_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ 麥克風錄音")
            file_input = gr.Audio(sources=["upload"], type="filepath", label="📂 上傳檔案")

        output_text = gr.Textbox(label="📝 辨識結果")
        
        # Action parts
        submit_btn = gr.Button("轉換")
        submit_btn.click(
            fn=transcribe_audio,
            inputs=[mic_input, file_input, backend_dropdown, language_dropdown, modelsize_dropdown],
            outputs=output_text
        )

        backend_dropdown.change(
            fn=update_model_size_dropdown,
            inputs=backend_dropdown,
            outputs=modelsize_dropdown
        )

    return app


def parse_args():
    parser = argparse.ArgumentParser(description="Multi-ASR Toolkit", add_help=True)
    parser.add_argument(
        "--mode",
        choices=["cli", "web"],
        default="web",
        help="選擇執行模式：cli 或 web (Gradio UI)，預設為 web"
    )
    known_args, remaining_args = parser.parse_known_args()
    return known_args, remaining_args


def main():
    known_args, remaining_args = parse_args()
    if known_args.mode == "cli":
        run_cli(remaining_args)
    else:
        # Launch the app
        # Gradio defaults to localhost:7860
        demo = build_demo()
        demo.queue()
        # To create a public link, set share=True
        demo.launch()


if __name__ == "__main__":
    main()
