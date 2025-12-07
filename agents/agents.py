from agents.system_prompt import create_system_prompt
from agents.utils import agent

def sleep_agent(prompt , previous_responses = None):
    system_prompt = create_system_prompt("Sleep")
    response = agent(prompt , system_prompt , previous_responses)

    return response

def exercise_agent(prompt , previous_responses = None):
    system_prompt = create_system_prompt("Exercise")
    response = agent(prompt , system_prompt , previous_responses)

    return response

def diet_agent(prompt , previous_responses = None):
    system_prompt = create_system_prompt("Diet")
    response = agent(prompt , system_prompt , previous_responses)

    return response

def medical_agent(prompt , previous_responses = None):
    system_prompt = create_system_prompt("Medical")
    response = agent(prompt , system_prompt , previous_responses)

    return response