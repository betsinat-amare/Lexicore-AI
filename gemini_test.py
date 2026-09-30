from google import genai
from dotenv import load_dotenv


load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="In one sentence, explain what speaker diarization does."
)

print(response.text)