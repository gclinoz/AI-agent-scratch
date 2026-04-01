import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import argparse

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="Enter user prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
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

success_flag = False
for _ in range(20):
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )

    if response.usage_metadata == None:
        raise RuntimeError("API request fail")
    
    if response.candidates:
        for res in response.candidates:
            messages.append(res.content)

    if args.verbose:
        if response.function_calls == None:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"Response:\n{response.text}")
            success_flag = True
            break
        else:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            function_responses = []
            
            for fn in response.function_calls:
                function_call_result = call_function(fn)
                if len(function_call_result.parts) == 0:
                    raise Exception("Empty function result parts list")

                if function_call_result.parts[0].function_response == None:
                    raise Exception("First item in the list of parts is None")

                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Actucal function result is None")

                function_responses.append(function_call_result.parts[0])
                print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_responses))

    if response.function_calls == None:
        print(f"Response:\n{response.text}")
        success_flag = True
        break
    else:
        function_responses = []
        
        for fn in response.function_calls:
            function_call_result = call_function(fn)
            if len(function_call_result.parts) == 0:
                raise Exception("Empty function result parts list")

            if function_call_result.parts[0].function_response == None:
                raise Exception("First item in the list of parts is None")

            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Actucal function result is None")

            function_responses.append(function_call_result.parts[0])

        messages.append(types.Content(role="user", parts=function_responses))

if success_flag:
    print("Task complete")
else:
    sys.exit("Task Fail. Maximum number of iterations is reached")
