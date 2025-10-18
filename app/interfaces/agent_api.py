from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..agent_network import AgentNetwork

router = APIRouter()
network = AgentNetwork()
agentA = network.register("Ares")
agentB = network.register("Athena")
network.start()

@router.get("/agents")
def list_agents():
    return JSONResponse({"agents": list(network.agents.keys())})

@router.post("/agents/negotiate")
async def negotiate(req: Request):
    body = await req.json()
    agent_name = body.get("agent", "Ares")
    state = body.get("state", {})
    agent = network.agents.get(agent_name)
    result = agent.negotiate(state)
    return JSONResponse({"result": result})
