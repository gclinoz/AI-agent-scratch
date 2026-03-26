import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="Enter user prompt")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)

messages = [types.Content(
        role="user",
        parts=[types.Part(text=args.user_prompt)]
    )
]
response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages
)

if response.usage_metadata == None:
    raise RuntimeError("API request fail")

print(f"User prompt: {args.user_prompt}")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Response:\n{response.text}")
