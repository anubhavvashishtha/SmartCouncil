from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

secret_value_0 = os.getenv("hf_token")

def agent(prompt, system_prompt, previous_responses=None):
    client = InferenceClient(api_key=secret_value_0)

    messages = [system_prompt]

    if previous_responses:
        messages.append({
            "role": "system",
            "content": f"Here are previous completed tasks for context:\n{previous_responses}"
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=messages
    )

    response = completion.choices[0].message.content.strip()
    return response