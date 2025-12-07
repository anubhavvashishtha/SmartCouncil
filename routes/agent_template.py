from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agents.agents import sleep_agent , exercise_agent , medical_agent , diet_agent

class PromptRequest(BaseModel):
    prompt: str                # task description
    original_prompt: str       # the user's actual input
    previous_tasks: list               # id of the task being processed
    max_tokens: Optional[int] = 100
    task_id: str
    agent:str

class PromptResponse(BaseModel):
    success: bool
    response: str
    agent_name: str
    prompt_received: str
    original_prompt: str
    task_id: str

def create_agent(agent_name: str, port: int):
    app = FastAPI(title=f"{agent_name} API", version="1.0.0")
    
    @app.get("/")
    async def root():
        return {
            "message": f"Welcome to {agent_name}",
            "agent": agent_name,
            "port": port
        }
    
    @app.post("/request", response_model=PromptResponse)
    async def handle_request(request: PromptRequest):
        try:
            if not request.prompt.strip():
                raise HTTPException(status_code=400, detail="Prompt cannot be empty")
            
            prompt = f"Original User Request : {request.original_prompt} , Taking this as context about user you need to solve this task : {request.prompt}"
            response = None
            
            if request.agent == "Sleep":
                response = sleep_agent(prompt , request.previous_tasks)
            if request.agent == "Exercise":
                response = exercise_agent(prompt , request.previous_tasks)
            if request.agent == "Diet":
                response = diet_agent(prompt , request.previous_tasks)
            if request.agent == "Medical":
                response = medical_agent(prompt , request.previous_tasks)
            
            # Agent response simulation
            demo_response = (
                f"[{agent_name}] Completed task {request.task_id}: "
                f"Processed '{prompt}...'"
            )
            
            return PromptResponse(
                success=True,
                response=response,
                agent_name=agent_name,
                prompt_received=prompt,
                original_prompt=request.original_prompt,
                task_id=request.task_id
            )
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "agent": agent_name}
    
    return app
