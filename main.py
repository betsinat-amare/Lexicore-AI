import json

from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI(title="LexiCore AI")


@app.get("/")
def root():
    return {
        "message": "LexiCore AI API is running"
    }


@app.get("/analysis")
def get_analysis():
    with open("analysis.json", "r", encoding="utf-8") as file:
        analysis = json.load(file)

    with open("combined_transcript.json", "r", encoding="utf-8") as file:
        transcript = json.load(file)

    return {
        "transcript": transcript,
        "findings": analysis["findings"],
    }


@app.get("/video")
def get_video():
    return FileResponse(
        "test.mp4",
        media_type="video/mp4"
    )