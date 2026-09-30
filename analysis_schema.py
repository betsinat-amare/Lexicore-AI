from pydantic import BaseModel
from typing import List


class Finding(BaseModel):
    policy: str
    category: str
    severity: str
    description: str
    evidence: str
    start: float
    end: float


class AnalysisResult(BaseModel):
    findings: List[Finding]