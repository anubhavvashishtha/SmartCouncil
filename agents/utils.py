from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

secret_value_0 = os.getenv("hf_token")

def agent(prompt , system_prompt):
    client = InferenceClient(api_key=secret_value_0)

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            system_prompt,
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    response = completion.choices[0].message.content.strip()
    return response