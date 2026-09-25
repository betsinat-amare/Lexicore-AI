import json

from pyannote.audio import Pipeline


pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1"
)

output = pipeline("test.wav")

speakers = []

for turn, speaker in output.speaker_diarization:
    speakers.append(
        {
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker,
        }
    )

with open("speakers.json", "w", encoding="utf-8") as file:
    json.dump(speakers, file, indent=2)

print("Diarization complete.")
print("Saved to speakers.json")