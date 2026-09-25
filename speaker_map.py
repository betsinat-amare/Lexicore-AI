import json


with open("combined_transcript.json", "r", encoding="utf-8") as file:
    transcript = json.load(file)


speaker_map = {}
next_number = 1

for segment in transcript:
    speaker = segment["speaker"]

    if speaker == "UNKNOWN":
        continue

    if speaker not in speaker_map:
        speaker_map[speaker] = f"Speaker {next_number}"
        next_number += 1


for segment in transcript:
    speaker = segment["speaker"]

    if speaker in speaker_map:
        segment["speaker_name"] = speaker_map[speaker]
    else:
        segment["speaker_name"] = "Unknown"


with open("combined_transcript.json", "w", encoding="utf-8") as file:
    json.dump(transcript, file, indent=2, ensure_ascii=False)


print("Speaker names assigned.")
print("\nSpeaker mapping:")

for original, name in speaker_map.items():
    print(f"{original} -> {name}")

print("\nUpdated combined_transcript.json")