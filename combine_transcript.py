import json


with open("transcript.json", "r", encoding="utf-8") as file:
    transcript = json.load(file)

with open("speakers.json", "r", encoding="utf-8") as file:
    speakers = json.load(file)


combined = []

for segment in transcript["segments"]:
    segment_start = segment["start"]
    segment_end = segment["end"]

    best_speaker = "UNKNOWN"
    best_overlap = 0

    for turn in speakers:
        overlap_start = max(segment_start, turn["start"])
        overlap_end = min(segment_end, turn["end"])

        overlap = max(0, overlap_end - overlap_start)

        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = turn["speaker"]

    combined.append(
        {
            "start": segment_start,
            "end": segment_end,
            "speaker": best_speaker,
            "text": segment["text"].strip(),
        }
    )


with open("combined_transcript.json", "w", encoding="utf-8") as file:
    json.dump(combined, file, indent=2, ensure_ascii=False)


print("Transcript and speakers combined.")
print("Saved to combined_transcript.json")