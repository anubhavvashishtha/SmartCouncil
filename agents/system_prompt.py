import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agent_cards import agent_cards

def create_system_prompt(name):
    agents = agent_cards['agents']
    
    agent_data = next((agent for agent in agents if agent['name'] == name), None)
    
    if agent_data is None:
        raise ValueError(f"Agent '{name}' not found in agent_cards")
    
    return {
        "role": "system",
        "content": f"""You are an AI agent named {agent_data["name"]}.

Primary Focus: {agent_data["focus"]}

Responsibilities:
{agent_data["responsibilities"]}

STRICT GUIDELINES:
- You ONLY answer questions directly related to: {agent_data["focus"]}
- If a question is outside your domain, respond EXACTLY with: "This question is outside my area of expertise. Please consult the [appropriate agent type] agent."
- Stay strictly within your responsibilities listed above"""
    }