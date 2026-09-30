from analysis_schema import AnalysisResult


result = AnalysisResult(
    findings=[
        {
            "policy": "Confidentiality",
            "category": "Potentially Relevant Statement",
            "severity": "high",
            "description": "The speaker describes an intention to commit a robbery.",
            "evidence": "Well, today we're gonna rob an apartment.",
            "start": 54.8,
            "end": 58.0,
        }
    ]
)


print(result.model_dump_json(indent=2))