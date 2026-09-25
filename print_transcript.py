import json


with open("combined_transcript.json", "r", encoding="utf-8") as file:
    transcript = json.load(file)


print("\n--- Speaker-Labeled Transcript ---\n")

for segment in transcript:
    start = segment["start"]
    end = segment["end"]
    speaker = segment["speaker_name"]
    text = segment["text"]

    print(
        f"[{start:06.2f}s - {end:06.2f}s] "
        f"{speaker}: {text}"
    )