import json
import whisper

model = whisper.load_model("base")

result = model.transcribe("test.mp4")

with open("transcript.json", "w", encoding="utf-8") as file:
    json.dump(result, file, indent=2, ensure_ascii=False)

print("Transcription complete.")
print("Saved to transcript.json")