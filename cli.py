import argparse
from backends import get_backend


def run_cli(args):
    parser = argparse.ArgumentParser(description="Run Multi-ASR Toolkit in CLI mode")

    parser.add_argument("audio_path", help="輸入的音訊檔案路徑（支援 mp3, wav 等）")
    parser.add_argument("--backend", choices=["transformers", "faster-whisper", "whisper", "speech-recognition"],
                        default="transformers", help="選擇辨識後端")
    parser.add_argument("--language", default="auto", help="語音語言（如 zh, en, ja, ko）")
    parser.add_argument("--model-size", default="small", help="模型大小，例如 small、medium、large")

    args = parser.parse_args()

    # 設定模型名稱（某些 backend 不需要）
    if args.backend == "transformers":
        model_name = f"openai/whisper-{args.model_size}"
    elif args.backend == "speech-recognition":
        model_name = None
    else:
        model_name = args.model_size

    # 準備 backend
    kwargs = {"language": args.language}
    if model_name:
        kwargs["model_size"] = model_name

    asr = get_backend(args.backend, **kwargs)

    print(f"[INFO] 使用 {args.backend} 後端進行辨識...")
    text = asr.transcribe(args.audio_path)
    print("\n📝 辨識結果：\n")
    print(text)
