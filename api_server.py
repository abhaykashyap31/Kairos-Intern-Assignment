from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_host import AgentHost
from typing import List

app = FastAPI()

# Allow CORS for local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[str] = []

agent = AgentHost()

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    tool_logs = []
    # Patch AgentHost to capture tool call logs
    def log_tool_call(tool_name, args, outcome=None, timestamp=None, latency=None):
        tool_logs.append(f"{tool_name} | Args: {args} | Outcome: {outcome}")
    old_log_tool_call = agent.log_tool_call
    agent.log_tool_call = log_tool_call
    try:
        response_lines = []
        for line in agent.handle_user_message(req.message):
            response_lines.append(line)
        response = "\n".join(response_lines)
    finally:
        agent.log_tool_call = old_log_tool_call
    return ChatResponse(response=response, tool_calls=tool_logs) 