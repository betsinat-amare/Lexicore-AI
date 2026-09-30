from google import genai
from dotenv import load_dotenv

from analysis_schema import AnalysisResult


load_dotenv()

client = genai.Client()

transcript = """
[054.80s - 058.00s] Speaker 2: The weather is really nice today.
[058.00s - 062.20s] Speaker 3: Yeah, I think we should go for a walk.
[062.20s - 065.00s] Speaker 2: Maybe we can get coffee afterward.
"""


policies = {
    "Confidentiality": (
        "Disclosure or discussion of confidential business information, "
        "private documents, credentials, internal data, or information "
        "explicitly identified as confidential."
    ),
    "Intellectual Property": (
        "Discussion involving proprietary software, inventions, patents, "
        "trade secrets, source code, copyrighted material, or ownership "
        "of intellectual property."
    ),
    "Financial Information": (
        "Discussion of financial records, account information, transactions, "
        "prices, payments, budgets, or other sensitive financial data."
    ),
    "Regulatory Discussion": (
        "Discussion of regulations, regulatory requirements, audits, "
        "compliance obligations, or interactions with regulators."
    ),
    "Sensitive Personal Information": (
        "Disclosure of sensitive personal information such as identification "
        "numbers, private contact information, health information, or other "
        "personally sensitive data."
    ),
}


prompt = f"""
Analyze the following transcript according to these policies:

{policies}

A finding must have a clear and direct connection to one of the
selected policies.

Do NOT classify content under a policy merely because the content
is sensitive, illegal, unusual, or important.

For each finding:
- Identify which policy it relates to.
- Give a category.
- Give a severity: low, medium, or high.
- Briefly explain why it was identified.
- Quote the relevant transcript as evidence.
- Preserve the exact start and end timestamps.

Only identify findings supported by the transcript.
Do not invent information.

If the transcript does not clearly relate to any of the policies,
return an empty findings list.

Transcript:
{transcript}
"""


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": AnalysisResult,
    },
)


result = AnalysisResult.model_validate_json(response.text)

print("\n--- AI Analysis ---\n")
print(result.model_dump_json(indent=2))