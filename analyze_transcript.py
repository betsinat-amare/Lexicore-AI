import json

from google import genai
from dotenv import load_dotenv

from analysis_schema import AnalysisResult


load_dotenv()

client = genai.Client()


with open("combined_transcript.json", "r", encoding="utf-8") as file:
    transcript = json.load(file)


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


transcript_text = "\n".join(
    f"[{segment['start']:.2f}s - {segment['end']:.2f}s] "
    f"{segment['speaker_name']}: {segment['text']}"
    for segment in transcript
)


prompt = f"""
Analyze the following speaker-labeled transcript according to these policies:

{policies}

A finding must have a clear and direct connection to the definition
of one of the policies.

The policy must be supported by the actual words in the relevant
transcript evidence.

Do NOT infer a policy connection from the surrounding story, context,
speaker intentions, or assumptions.

Ask this question for every potential finding:

"If the surrounding conversation were removed, would the quoted
evidence by itself still clearly match the policy definition?"

If the answer is no, do not create a finding.

Do NOT classify content merely because it is sensitive, unusual,
illegal, valuable, important, or related to a potentially risky event.

For example, mentioning jewels, money, or an apartment does NOT
automatically qualify as Financial Information. Financial Information
requires discussion of financial records, accounts, transactions,
payments, prices, budgets, or similar financial data.

Only create a finding when the evidence itself provides a clear
policy-specific connection.

For each finding:
- Identify the relevant policy.
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
{transcript_text}
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


with open("analysis.json", "w", encoding="utf-8") as file:
    json.dump(
        result.model_dump(),
        file,
        indent=2,
        ensure_ascii=False,
    )


print("AI analysis complete.")
print("Saved to analysis.json")
print(f"Findings: {len(result.findings)}")