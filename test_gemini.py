import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

print("TEST STARTED", flush=True)

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: GOOGLE_API_KEY missing in .env", flush=True)
    raise SystemExit(1)

print("API key loaded.", flush=True)

client = genai.Client(api_key=api_key)

try:
    print("Sending request to Gemini...", flush=True)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Reply with exactly: GEMINI WORKING",
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=50,
        ),
    )

    print("SUCCESS:", response.text, flush=True)

except Exception as error:
    print("GEMINI ERROR:", type(error).__name__, str(error), flush=True)

finally:
    client.close()

print("TEST FINISHED", flush=True)
